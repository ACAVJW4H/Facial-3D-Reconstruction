#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 13:13:50 2018

@author: mingqian
"""

import rawpy
import os
import imageio
import colorsys
import math
from math import sin,cos,pi
import numpy as np
from PIL import Image
from PIL import ImageFilter
from numpy import linalg as LA
from sklearn.preprocessing import normalize

DATA_FOLDER = "."

def whiteBalanceImage(im,kR,kG,kB):
    balancedR = kR * im[...,0]
    balancedG = kG * im[...,1]
    balancedB = kB * im[...,2]
    balancedIm = np.empty_like(im).astype("float64")
    balancedIm[...,0] = balancedR
    balancedIm[...,1] = balancedG
    balancedIm[...,2] = balancedB
    return np.clip(balancedIm,0,255)
    
def saveImage(im, name):
    im = Image.fromarray(im.astype('uint8'))
    im.save(name)

#compute specular albedo#############################################################################

#c = max(r,g,b) - min(r,g,b)
#compute c for each pixel
def computeChroma(im_rgb):
    im_rgb = im_rgb / 255.0
    height, width, _ = im_rgb.shape
    chroma = np.zeros((height, width))
    for h in range(height):
        for w in range(width):
            r, g, b = im_rgb[h,w,...]
            chroma[h, w] = max(r,g,b)- min(r,g,b)
    return chroma

#h, s, and v range from 0 - 1
def rgb2hsv(im_rgb):
    im_rgb = im_rgb / 255.0
    im_hsv = np.empty_like(im_rgb).astype("float64")
    height, width, _ = im_rgb.shape
    for h in range(height):
        for w in range(width):
            #im_hsv[h,w,...] = colorsys.rgb_to_hsv(im_rgb[h,w,0], im_rgb[h,w,1], im_rgb[h,w,2])
            hsv = colorsys.rgb_to_hsv(im_rgb[h,w,0], im_rgb[h,w,1], im_rgb[h,w,2])
            im_hsv[h,w,0] = hsv[0]
            im_hsv[h,w,1] = hsv[1]
            im_hsv[h,w,2] = hsv[2]
    return im_hsv

def computeDelta(grad, comp):
    grad_hsv = rgb2hsv(grad)
    comp_hsv = rgb2hsv(comp)
    V_g = grad_hsv[...,2]
    S_c = comp_hsv[...,1]
    C_g = computeChroma(grad)
    delta = V_g - np.divide(C_g, S_c,out=np.zeros_like(C_g), where=S_c!=0)
    return np.clip(delta, 0, 1.0)

#compute the specular albedo as the average of delta_X and delta_Y
def computeSpecAlbedo(delta_X, delta_Y):
    return (delta_X + delta_Y) / 2.0

#combime the bright half of the gradient with the bright half of the complement
#output image pixels range 0-255
def createDiffSpecImage(grad, comp):
    height, width, _ = grad.shape
    grad_hsv = rgb2hsv(grad)
    comp_hsv = rgb2hsv(comp)
    new = np.empty_like(grad).astype("float64")
    for h in range(height):
        for w in range(width):
            if(grad_hsv[h,w,2] > comp_hsv[h,w,2]):
                new[h,w,...] = grad[h,w,...]
            else:
                new[h,w,...] = comp[h,w,...]
    return new

def createDiffOnlyImage(grad, comp):
    height, width, _ = grad.shape
    grad_hsv = rgb2hsv(grad)
    comp_hsv = rgb2hsv(comp)
    new = np.empty_like(grad).astype("float64")
    for h in range(height):
        for w in range(width):
            if(grad_hsv[h,w,2] <= comp_hsv[h,w,2]):
                new[h,w,...] = grad[h,w,...]
            else:
                new[h,w,...] = comp[h,w,...]
    return new

# X_diffSpec = createDiffSpecImage(b_X, b_rX)
# X_diffOnly = createDiffOnlyImage(b_X, b_rX)
# Y_diffSpec = createDiffSpecImage(b_Y, b_rY)
# Y_diffOnly = createDiffOnlyImage(b_Y, b_rY)

# delta_X = computeDelta(X_diffSpec, X_diffOnly)
# delta_Y = computeDelta(Y_diffSpec, Y_diffOnly)

# specAlbedo = computeSpecAlbedo(delta_X, delta_Y)
# specAlbedo *= 255;
# saveImage(specAlbedo, "specularAlbedo.tif")

#compute diffuse albedo#############################################################################
def computeDiffAlbedo(mixed, spec):
    diffAlbedo = np.empty_like(mixed).astype("float64")
    diffAlbedo[...,0] = mixed[...,0] - spec
    diffAlbedo[...,1] = mixed[...,1] - spec
    diffAlbedo[...,2] = mixed[...,2] - spec
    return np.clip(diffAlbedo,0,255)
# fullOn = np.clip(X_diffSpec + X_diffOnly,0,255)
# diffAlbedo = computeDiffAlbedo(fullOn, specAlbedo)
# saveImage(diffAlbedo, "diffuseAlbedo.tif")


#compute normals###########################################################################
def computeAlpha(cp, pp):
    #only use the blue channel of the mixed albedo
    diff = cp[...,1]
    diffSpec = pp[...,1]
    return np.divide(diff, diffSpec, np.zeros_like(diff), where=(diffSpec)!=0)

def computeReflectionVector(mixedNormals,uvNormals, alpha):
    rVector = np.empty_like(mixedNormals).astype("float64")
    height, width = alpha.shape
    uvNormals_copy = np.empty_like(uvNormals).astype("float64")
    for h in range(height):
        for w in range(width):
            uvNormals_copy[h,w,...] = alpha[h,w] * uvNormals[h,w,...]
    rVector[...,0] = mixedNormals[...,0] - uvNormals_copy[...,0]
    rVector[...,1] = mixedNormals[...,1] - uvNormals_copy[...,1]
    rVector[...,2] = mixedNormals[...,2] - uvNormals_copy[...,2]
    
    for k in range(height):
        normalize(rVector[k], copy=False)
    
    return rVector

def computeSpecularNormals(rVector):
    specNormals = np.empty_like(rVector).astype("float64")
    height, width, _ = specNormals.shape
    specNormals[...,0] = rVector[...,0]
    specNormals[...,1] = rVector[...,1]
    specNormals[...,2] = rVector[...,2]
    for h in range(height):
        for w in range(width):
            specNormals[h,w,2] += 1
    for h in range(height):
        normalize(specNormals[h], copy=False)
    return specNormals

def cart2sph(x,y,z):
    azimuth = np.arctan2(y,x)
    elevation = np.arctan2(z,np.sqrt(x**2 + y**2))
    r = np.sqrt(x**2 + y**2 + z**2)
    return azimuth, elevation, r

def buildr(psi,dir):
	R = np.zeros((3,3))
	N= LA.norm(dir)
	l=dir[0]/N
	m=dir[1]/N
	n=dir[2]/N
	R[0,0]=cos(psi)+(1-cos(psi))*(l**2)
	R[0,1]=l*m*(1-cos(psi))+n*sin(psi)
	R[0,2]=l*n*(1-cos(psi))-m*sin(psi)
	R[1,0]=l*m*(1-cos(psi))-n*sin(psi)
	R[1,1]=cos(psi)+(1-cos(psi))*(m**2)
	R[1,2]=m*n*(1-cos(psi))+l*sin(psi)
	R[2,0]=l*n*(1-cos(psi))+m*sin(psi)
	R[2,1]=m*n*(1-cos(psi))-l*sin(psi)
	R[2,2]=cos(psi)+(1-cos(psi))*(n**2)
	return R


def rgb2suv(im_rgb):
	#source color
	s = np.array((1,1,1))
	s = s / LA.norm(s)

	az, el, _ = cart2sph(s[0],s[1],s[2])
	R = buildr((pi/2-el), np.array((0,1,0))) * buildr(az, np.array((0,0,1)))
	R = np.matmul(buildr((pi/2-el), np.array((0,1,0))), buildr(az, np.array((0,0,1))))
	R = np.flipud(R)
	
	height, width, _ = im_rgb.shape
	im_rgb = np.reshape(im_rgb, (height * width, 3))
	im_rgb = np.transpose(im_rgb)
	im_suv = np.matmul(R, im_rgb)
	im_suv = np.transpose(im_suv)
	im_suv = np.reshape(im_suv, (height, width, 3))

	return im_suv

#correct the specular normals 
# =============================================================================
# specNormals = Image.open("specularNormals.tif")
# specNormalsBlured = specNormals.filter(ImageFilter.GaussianBlur(30))
# 
# specNormals = np.array(specNormals).astype("float64")
# sapecNormalsBlured = np.array(specNormalsBlured).astype("float64")
# highpass = specNormals - specNormalsBlured
# correctedSpecNormals = np.clip(diffuseNormals + highpass, 0, 255)
# saveImage(correctedSpecNormals, "correctedSpecularNormals.tif")
# =============================================================================

def calculateNormals(card=4):
   
    # Import Photos
    b_X = np.array(Image.open("X_linear.tif")).astype("float64")
    b_rX = np.array(Image.open("RX_linear.tif")).astype("float64")
    b_Y = np.array(Image.open("Y_linear.tif")).astype("float64")
    b_rY = np.array(Image.open("RY_linear.tif")).astype("float64")
    b_Z = np.array(Image.open("Z_linear.tif")).astype("float64")
    b_rZ = np.array(Image.open("RZ_linear.tif")).astype("float64")
    b_Full_cp = np.array(Image.open("FULL_cp_linear.tif")).astype("float64")
    b_Full_pp = np.array(Image.open("FULL_pp_linear.tif")).astype("float64")

    # Get UVs
    X_suv = rgb2suv(b_X)
    X_uv = np.sqrt(X_suv[...,1]**2 + X_suv[...,2]**2)
    rX_suv = rgb2suv(b_rX)
    rX_uv = np.sqrt(rX_suv[...,1]**2 + rX_suv[...,2]**2)
    Y_suv = rgb2suv(b_Y)
    Y_uv = np.sqrt(Y_suv[...,1]**2 + Y_suv[...,2]**2)
    rY_suv = rgb2suv(b_rY)
    rY_uv = np.sqrt(rY_suv[...,1]**2 + rY_suv[...,2]**2)
    Z_suv = rgb2suv(b_Z)
    Z_uv = np.sqrt(Z_suv[...,1]**2 + Z_suv[...,2]**2)
    rZ_suv = rgb2suv(b_rZ)
    rZ_uv = np.sqrt(rZ_suv[...,1]**2 + rZ_suv[...,2]**2)

    N_x = X_uv - rX_uv
    N_y = Y_uv - rY_uv
    N_z = Z_uv - rZ_uv

    diffuseNormals = np.empty_like(b_X).astype("float64")
    diffuseNormals[..., 0] = N_x
    diffuseNormals[..., 1] = N_y
    diffuseNormals[..., 2] = N_z

    height, width, _ = b_X.shape
    for h in range(height):
        normalize(diffuseNormals[h], copy=False)
    # =============================================================================
    # diffuseNormalsBlured = np.array(Image.open("blured.ppm")).astype("float64")
    # diffuseNormalsBlured /= 255.0
    # diffuseNormalsBlured *= 2.0
    # diffuseNormalsBlured -= 1
    # for h in range(height):
    # 	normalize(diffuseNormalsBlured[h], copy=False)
    # =============================================================================
        
    N_x = (b_X - b_rX) 
    N_y = (b_Y - b_rY) 
    N_z = (b_Z - b_rZ) 

    mixedNormals = np.empty_like(N_x).astype("float64")

    #mixed normals using blue channel
    mixedNormals[..., 0] = N_x[..., 1]
    mixedNormals[..., 1] = N_y[..., 1]
    mixedNormals[..., 2] = N_z[..., 1]

    height, width, _ = b_X.shape
    for h in range(height):
        normalize(mixedNormals[h], copy=False)
        
    alpha = computeAlpha(b_Full_cp, b_Full_pp)
    rVector = computeReflectionVector(mixedNormals, diffuseNormals, alpha)
    specNormals = computeSpecularNormals(rVector)

    specNormals = (specNormals + 1.0) / 2.0
    specNormals *= 255.0
    mixedNormals = (mixedNormals + 1.0) / 2.0
    mixedNormals *= 255.0
    diffuseNormals = (diffuseNormals + 1.0) / 2.0
    diffuseNormals *= 255.0

    saveImage(specNormals,"specularNormals.tif")
    saveImage(diffuseNormals,"diffuseNormals.tif")
    saveImage(mixedNormals,"mixedNormals.tif")

calculateNormals()