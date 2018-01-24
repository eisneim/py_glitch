#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" py_glich

the old school way to glitch a media file(image, audio, video) by 特里(vidBuddy视频大拍档)
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import random

DEFAULT_HEADER_SIZE = 200
# HEADER_SIZE = { "jpg": 9, "png": 8, "gif": 14, "tiff": 8, "bmp": 54, "mp4": 128 }

def destroy(input, outFile, intensity=0.1, bufferSize=100, headerSize=DEFAULT_HEADER_SIZE):
  with open(input, "rb") as fin:
    with open(outFile, "wb") as fout:
      # protect the header
      fout.write(fin.read(headerSize))
      while True:
        inByte = fin.read(bufferSize)
        if not inByte:
          break
        if (random.random() < intensity / 100):
          outByte = os.urandom(bufferSize)
          #outbyte = '\x0a'
        else:
          outByte = inByte

        fout.write(outByte)

def main():
  parser = argparse.ArgumentParser(description="破坏媒体文件，生成glitch效果的新文件")
  parser.add_argument("input", metavar="i", type=str,
    help="源文件的路径")
  parser.add_argument("output", type=str, nargs="*", default=[], help="输出文件夹的路径，默认为源文件所在文件夹")
  parser.add_argument("--intensity", type=float, dest="intensity", default=0.1,
    help="强度，默认为0.1")
  parser.add_argument("--buffer", type=int, default=100, dest="bufferSize",
    help="一次性随机的数据的大小，buffer越大，速度越快，图片适合10以下，视频适合使用100以上; buffer越大，速度越快，glitch越不明显")
  parser.add_argument("--count", type=int, dest="count", default=1,
    help="生成多少个文件")
  parser.add_argument("--header", type=int, default=DEFAULT_HEADER_SIZE, dest="headerSize",
    help="文件头部信息的大小，默认200，图片的header一般很小；破坏header将导致文件无法识别")

  args = parser.parse_args()
  if not os.path.exists(args.input):
    raise ValueError("源文件不存在")
  # print(args)
  outPath = args.output[0] if len(args.output) > 0 else os.path.dirname(args.input)

  ext = os.path.splitext(args.input)[1]
  filename = os.path.basename(args.input).split(".")[0]

  for ii in range(args.count):
    outName = "{name}_{idx}{ext}".format(name=filename, idx=ii, ext=ext)
    outFile = os.path.join(outPath, outName)
    destroy(args.input, outFile, args.intensity, args.bufferSize, args.headerSize)

  print(">> 完成")

if __name__ == "__main__":
  main()