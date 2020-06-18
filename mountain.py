#!/usr/local/bin/python3
#
# Authors: [PLEASE PUT YOUR NAMES AND USER IDS HERE]
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2019
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import copy as dp
import time as t

def exp_fun(x, l):
    return l * exp(-l * abs(x))


# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale, 0, filtered_y)
    return sqrt(filtered_y ** 2)


# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    image_edge = dp.deepcopy(image)
    for (x, y) in enumerate(y_coordinates):
        for t in range(int(max(y - int(thickness / 2), 0)), int(min(y + int(thickness / 2), image_edge.size[1] - 1))):
            image_edge.putpixel((x, t), color)
    return array(image_edge)


# Method-1
# P(Si|W1,W2,...Wm) ~ P(Si)*P(Wi/Si)
def simple(E, max_row, max_col):
    for col in range(max_col):
        ridge[col] = array(where(E[:, col] == amax(E[:, col])))
        if len(ridge[col][0]) > 1 and col > 0:
            ridge[col] = absolute(ridge[col] - ridge[col - 1]).min() + ridge[col - 1]
    return ridge


# Method-2  Viterbi algorithm
def viterbi(E, Trans_P, max_row, max_col):
    # V format [argmax prob ,Seq till now]
    V = [[[0, []] for col in range(max_col)] for row in range(max_row)]
    for row in range(max_row):
        V[row][0] = [log(E[row, 0] / max_row), [row]]
    for col in range(max_col - 1):
        for rowi in range(max_row):
            [max_arg_P, Max_arg_seq] = max(
                [[V[rowj][col][0] + log(Trans_P[rowi, rowj]), V[rowj][col][1]] for rowj in range(max_row)])
            V[rowi][col + 1][0] = log(E[rowi, col + 1]) + max_arg_P
            V[rowi][col + 1][1] = Max_arg_seq + [rowi]

    [max_arg_P, [Max_arg_seq]] = max([[V[row][max_col - 1][0], [V[row][max_col - 1][1]]] for row in range(max_row)])

    return Max_arg_seq


# main function
if __name__ == "__main__":
    start_time =t.time()
    (input_filename, gt_row, gt_col) = sys.argv[1:]

    # load in image
    input_image = Image.open(input_filename)
    # compute edge strength mask
    edge_strength = edge_strength(input_image)
    imageio.imwrite('edges.jpg', uint8(255 * edge_strength / (amax(edge_strength))))

    # You'll need to add code here to figure out the results! For now,
    # just create a horizontal centered line.
    ridge = [edge_strength.shape[0] / 2] * edge_strength.shape[1]
    max_col = edge_strength.shape[1]
    max_row = edge_strength.shape[0]
    P_far = 0.00001
    high_prob_rows = 7
    E = dp.deepcopy(edge_strength)
    E=array([[col if col>0 else pow(10, -100) for col in row ]for row in E])
    Trans_P = ones((max_row, max_row))
    for col in range(max_col):
        E[:, col] = E[:, col] / sum(edge_strength[:, col])

    for rowi in range(max_row):
        highP_rows = []
        highP_rows_sum = 0
        for rowj in range(max_row):
            Trans_P[rowi, rowj] = exp_fun(rowj - rowi, 3.5)
        sum_rowP = sum(Trans_P[rowi, :])
        for rowj in range(max_row):
            Trans_P[rowi, rowj] = Trans_P[rowi, rowj] / sum_rowP
    Trans_P_Viterbi = array([[(1 - (P_far * (max_row - high_prob_rows))) / high_prob_rows if -(
                high_prob_rows // 2) <= rowi - rowj <= (high_prob_rows // 2) else P_far for rowi in range(max_row)] for
                             rowj in range(max_row)])

    #    # Method -1
    ridge = simple(E, max_row, max_col)
    # output answer
    imageio.imwrite("output_simple.jpg", draw_edge(input_image, ridge, (0, 0, 255), 5))

    ##    #Method-2  Viterbi algorithm
    ##    #Vj(t+1) = ej(Ot+1)* max Vi(t)*Pij   (1<= i <= N)
    ridge = viterbi(E, Trans_P_Viterbi, max_row, max_col)
    # output answer
    imageio.imwrite("output_map.jpg", draw_edge(input_image, ridge, (255, 0, 0), 5))

    #    #Method-3  Human Feedback

    E[:, int(gt_col)] = pow(10, -100)
    E[int(gt_row), int(gt_col)] = 1 - (max_row - 1) * pow(10, -100)

    ridge = viterbi(E, Trans_P, max_row, max_col)

    # output answer
    imageio.imwrite("output_human.jpg", draw_edge(input_image, ridge, (0, 255, 0), 5))
    print(t.time()-start_time)