#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/12/8
"""
from lpp import *

import pandas as pd
if __name__ == '__main__':
    usage = '''usage: python2.7 %prog [options] 
		     Pilr-CR Crispr Finding！！！
		     '''
    
    parser = OptionParser(usage =usage )    
    parser.add_option("-g", "--Genome", action="store",
                      dest="Genome",
                      help="Genome Sequence")


    parser.add_option("-o", "--OUTPUT", action="store",
                      dest="outputprefix",
                      help="Output Path") 

    (options, args) = parser.parse_args()
    
    Genome = options.Genome
    outputprefix = options.outprefix
    