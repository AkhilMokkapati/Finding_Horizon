###  Horizon finding
1.	Simplest Bayes net approach: Using simple bayes net where each state(Si) is independent of one another and each observation(Wi) is just dependent on corresponding State(Si)
- Our observable values are from the intensities of edge strength image which is P(Si|Wi)
- To find the horizon of the given image, we just use the argmax of edge strength to find the ridge vector
![equation]( https://latex.codecogs.com/gif.latex?%5Cinline%20s_%7Bi%7D%5E%7B*%7D%20%3D%20arg%20%5Cmax_%7Bs_%7Bi%7D%7D%20P%28S_%7Bi%7D%3Ds_%7Bi%7D%7Cw_%7B1%2C...%2C%7Dw_%7Bm%7D%29%20%5C%5C%20s_%7Bi%7D%5E%7B*%7D%20%3D%20arg%20%5Cmax_%7Bs_%7Bi%7D%7D%20P%28S_%7Bi%7D%3Ds_%7Bi%7D%29*P%28S_%7Bi%7D%3Ds_%7Bi%7D%7Cw_%7Bi%7D%29)
- All rows are equally likely in each of the column, so P(Si) will be 1/n and therefore edge strength is enough to find the horizon in this case
- We directly take arg max of edge strength in each column and use this as ridge in our actual image
- This is a very simple case and it doesn’t give the best results because gradient could be highest for non-horizon cases also
2.	Viterbi algorithm to solve for the maximum a posterior estimate
- Similarly, Our observable values are from the intensities of edge strength image
- To find the horizon of image, we find the max edge strength row for each column by the method of Viterbi
- Here each column is time sequence, and each row is the state 
- Viterbi variables along with sequence with max probability to reach that state are stored in a matrix
- In this viterbi case:
  - Start probability for each row is 1/n where n is max number of rows 
  - Emission Probability:
  
  ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20e_%7Bi%7D%28O_%7Bj%7D%29%20%3D%20x_%7Bi%2Cj%7D/%5Csum_%20j%20x_%7Bi%2Cj%7D)
  - Transition Probability: 
  
  ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20P_%7Bij%7D%20%3D%20l*%5Cexp%5E%7B-l*%7Cx%7C%7D%20%5C%20where%20%5C%20x%20%3D%20i-j)
  
  After trying out different values for parameter(l), we finally chose l = 3.5
  
  
- Major challenges faced are with the images that have a continuous higher gradient shift for non-horizon segments of the image
3.	Human feedback case - We follow the same steps as Viterbi, except that we take emission probability at (x,y) as 1 to force the horizon pass through this point (x,y) 
