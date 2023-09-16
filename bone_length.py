import torch
import matplotlib.pyplot as plt
import numpy as np

keypoints = ['nose', 'middle', 'head_top', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']
# [[0,1], [1,2], [3,4],[4,5], [3,6], [6,0], [13,3], [10, 0], [13, 7], [7, 10], [8, 7], [9, 8], [10, 11], [11,12],[13,14],[14,15]]
joint_keys = [('head_top', 'nose'), ('nose', 'middle'), ('middle', 'left_shoulder'), ('middle', 'right_shoulder'), ('left_shoulder', 'left_elbow'), ('right_shoulder', 'right_elbow'), ('left_elbow', 'left_wrist'), ('right_elbow', 'right_wrist'), ('left_shoulder', 'left_hip'), ('right_shoulder', 'right_hip'), ('left_hip', 'left_knee'), ('right_hip', 'right_knee'), ('left_knee', 'left_ankle'), ('right_knee', 'right_ankle')]
'''
joint_sym = [('head_top', 'nose'), ('nose', 'middle'), ('middle', 'left_shoulder'), ('middle', 'right_shoulder'), ('left_shoulder', 'left_elbow'), ('right_shoulder', 'right_elbow'), ('left_elbow', 'left_wrist'), ('right_elbow', 'right_wrist'), ('left_shoulder', 'left_hip'), ('right_shoulder', 'right_hip'), ('left_hip', 'left_knee'), ('right_hip', 'right_knee'), ('left_knee', 'left_ankle'), ('right_knee', 'right_ankle')]

joint_index = []

for jk in joint_keys:
    joint_index.append([keypoints.index(jk[0]), keypoints.index(jk[1])])
'''

joint_pairs_indices = [[2, 0], [0, 1], [1, 3], [1, 4], [3, 5], [4, 6], [5, 7], [6, 8], [3, 9], [4, 10], [9, 11], [10, 12], [11, 13], [12, 14]]

#dcpose_pair = [[2,0], [0,1], [1, 3], []]
def compute_bone_length(X):
    """
    computes bone lengths of the bones in the skeleton
    X is 3D joint estimates of shape N x H x K x C
    where N is the number of frames, H is the number of humans in the frame (1 in case of Human3.6M),
    K is the number of joints and C is x,y,z coordinates
    
    """
    '''
    X = X.reshape(X.shape[0], 3, len(keypoints))
    X = torch.unsqueeze(torch.transpose(X,1,2), 1)
    '''
    #shape N x H x B where B is the number of bones in the skeleton
    #skel = torch.zeros((X.shape[0], X.shape[1], len(keypoints)))
    skel = torch.zeros((X.shape[0], len(joint_pairs_indices)))
    #joint_pairs_indices = [[0,1], [1,2], [3,4],[4,5], [3,6], [6,0], [13,3], [10, 0], [13, 7], [7, 10], [8, 7], [9, 8], [10, 11], [11,12],[13,14],[14,15]]
    count = 0

    #print(X.shape)
    #stop
    for bone in joint_pairs_indices:
        skel[:, count] = torch.squeeze(torch.norm(X[:,bone[0],:] - X[:,bone[1], :], dim = 1))
        #skel[:, :, count] = (torch.sum(((X[:,:,bone[0]] - X[:,:,bone[1]])**2), dim = -1)**0.5)
        count += 1
    return skel         

    #loss calculation lambda_bone * criterion(skel[frame][human], skel[prev_frame][prev_human]).sum()

def skeleton_symmetry(X):
    
    skel_left = [2,4,6,8,10,12]
    skel_right = [3,5,7,9,11,13]
    norm = torch.norm(X[:, skel_left] - X[:, skel_right], dim = 1)
    mean_norm = torch.mean(norm)
    return mean_norm

#ALPHAPOSE           HUMAN3.6 data
#0 left hip          middle Hip    6 /
#1 left knee         right hip     3 /
#2 left foot         right knee    4 /
#3 right hip         right ankle   5 /
#4 right knee        left hip      0 /
#5 right foot        left knee     1 /
#6 middle hip        left ankle    2 /
#7 neck              spine           /
#8 nose              neck          7 /
#9 head              jaw           8 /
#10 left shoulder    head          9 /
#11 left elbow       left shoulder 10 /
#12 left wrist       left elbow    11 /
#13 right shoulder   left wrist    12 /
#14 right elbow      right showder 13
#15 right wrist      right elbow   14
#16                  right wrist   15
def compute_bone_length_human36m(X):
    """
    computes bone lengths of the bones in the skeleton
    X is 3D joint estimates of shape N x H x K x C
    where N is the number of frames, H is the number of humans in the frame (1 in case of Human3.6M),
    K is the number of joints and C is x,y,z coordinates
    
    """
    '''
    fig, ax1 = plt.subplots(1, 1)

    fig3d = plt.figure(400)
    fig3d.set_size_inches((5, 3))
    
    ax1 = fig3d.gca(projection='3d')
    '''
    #height_joints = [3]
    #human36_joints = [[0,1], [1,2], [3,4],[4,5], [3,6], [6,0], [13,3], [10, 0], [13, 7], [7, 10], [8, 7], [9, 8], [10, 11], [11,12],[13,14],[14,15]]
    human36_joints = [[5,6], [4,5], [0,4], [2, 3], [1,2], [0,1], [0,7], [7,8], [8,9], [9, 10], [13,12], [12, 11], [11,8], [16, 15], [15, 14], [14, 8]]
    skel = torch.zeros((X.shape[0], len(human36_joints)))

    #height_joints = [[5,6], [4,5], [0,7], [7,8], [8,10]]
    height_joints = [[5,6], [4,5], [0,8], [8,10]]
    '''
    for pair in human36_joints:
        ax1.plot([X[0, pair[0], 0].detach().numpy(), X[0, pair[1], 0].detach().numpy()] , [X[0, pair[0], 1].detach().numpy(), X[0, pair[1], 1].detach().numpy()] , [X[0, pair[0], 2].detach().numpy(), X[0, pair[1], 2].detach().numpy()])
    plt.show()
    '''
    count = 0

    #print(X.shape)
    #stop
    for bone in human36_joints:
        skel[:, count] = torch.squeeze(torch.norm(X[:,bone[0],:] - X[:,bone[1], :], dim = 1))
        count += 1

    height = torch.zeros((X.shape[0]))

    for bone in height_joints:
        height = height + torch.squeeze(torch.norm(X[:,bone[0],:] - X[:,bone[1], :], dim = 1))

    print(height, " hiehgts")
    stop
    return skel, height         
