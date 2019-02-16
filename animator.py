import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gdal
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('csvIn', help='The timestamped CSV location file')
args = parser.parse_args()

rawLocs = gdal.open(args.csvIn)
