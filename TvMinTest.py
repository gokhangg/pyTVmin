# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 19:42:09 2018

@author: Gokhan Gunay
"""


import sys
import argparse

from TvMin import TvMin
from ExternalLibs import ItkHandler

def main(argv):
    print("---------------------------------------------------")
    parser = argparse.ArgumentParser(
        description="Applies total variation minimization on the input image " +
                    "given the minimization parameters, and then " +
                    " writes the result to the given location with desired image format.\n")
    
    parser.add_argument(
        "--InFile", "-in",
        type=str,
        help="Input image file.")
    
    parser.add_argument(
        "--OutFile", "-out",
        type=str,
        help="Output image file.")
    
    parser.add_argument(
        "--Lambda", "-l",
        type=float,
        help="Lambda weight of the minimization algorithm.")
    
    parser.add_argument(
        "--To", "-to",
        type=float,
        help="To value of the minimization algorithm.")
    
    parser.add_argument(
        "--Iteration", "-it",
        type=int,
        help="Number of iterations in the minimization algorithm.")
    
    parser.add_argument(
        "--Verbose", "-v",
        type=bool,
        help="Used to print details of the procedure steps.")
    
    args = parser.parse_args()
    
    image_loader = ItkHandler.ItkHandler.loadItkImage
    image_saver = ItkHandler.ItkHandler.saveItkImage
    
    if not args.InFile is None:
        image = image_loader(args.InFile)
        print("Input file is :" + args.InFile)
        
        tv= TvMin.TvMin()
        tv.setInputImage(image[0])
        
        if not args.Lambda is None:
            tv.setLambda(args.Lambda)
            print("Lambda value is " + str(args.Lambda) + ".")
        else:
            print("Lambda value is not provided. Assigned 0 instead.")
            tv.setLambda(0.)
            
        if not args.To is None:
            tv.setTo(args.To)
            print("To value is " + str(args.To) + ".")
        else:
            print("To value is not provided. Assigned 0.15 instead.")
            tv.setTo(0.15)
            
        if not args.Iteration is None:
            print("Iteration number is " + str(args.Iteration) + ".")
            tv.setIterationNum(args.Iteration)
        else:
            print("Iteration number is not provided. Assigned 20 instead.")
            tv.setIterationNum(20)
        
        if not args.Verbose is None:
            print("Verbose is " + str(args.Verbose) + ".")
            tv.setVerbose(args.Verbose)
        else:
            print("Verbose is not provided. Assigned False instead.")
            tv.setVerbose(False)
            
        tv.minimize()
    
        print("Image shape: " + str(list(reversed((tv.getResultImage().shape)))) + ".\n")
        image_saver(args.OutFile, [tv.getResultImage(), image[1], image[2]])
        print("Output file is :" + args.OutFile)
            
        print("---------------------------------------------------")
        print("done")
        print("---------------------------------------------------")
    else:
        print("No input file provided. Please read help by typing --help.")


if __name__ == "__main__":
    main(sys.argv)
 