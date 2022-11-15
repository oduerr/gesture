



## We describe the transformation from a **fixed** coordinate system 
## in space to a Coordinate system in Body frame
#First we rotate g at original x-axis (this will be yaw)
#Second we rotate b around the new y-axis (this will be pitch)
#Third we rotate a around new z-axis (this will be roll)
from_fixed_to_body = function(a, b, g, degrees=TRUE){
    if (degrees){
      a = a * 2*pi / 360
      b = b * 2*pi / 360
      g = g * 2*pi / 360
    }
    Ra = matrix(
      c(cos(a), -sin(a), 0, sin(a), cos(a), 0, 0, 0, 1)
      , nrow=3, byrow = TRUE) 
    Rb = matrix(
      c(cos(b), 0, sin(b), 0, 1, 0, -sin(b), 0, cos(b))
      , nrow=3, byrow = TRUE) 
    Rg = matrix(
      c(1,0,0, 0, cos(g), -sin(g), 0, sin(g), cos(g))
      , nrow=3, byrow = TRUE) 
   return ((Ra %*% Rb) %*% Rg)
}
from_fixed_to_body(0,0,0) #Unit Matrix

###### Defining a Rotation Matrix in TensorFlow ###### 
from_fixed_to_body_tf = function(w){
  ca = tf$cos(w[1])
  sa = tf$sin(w[1])
  cb = tf$cos(w[2])
  sb = tf$sin(w[2])
  cb = tf$cos(w[2])
  sb = tf$sin(w[2])
  cg = tf$cos(w[3])
  sg = tf$sin(w[3])
  e = k_constant(1.)
  z = k_constant(0.)
  R = tf$reshape(c(
    ca*cb, ca*sb*sg - sa*cg, ca*sb*cg + sa*sg,
    sa*cb, sa*sb*sg + ca*cg, sa*sb*cg - ca*sg,
    -sb,    cb*sg,            cb*cg), shape=c(3L,3L))
  return (R)
}

show_coordinates = function(R){
  vec <- rbind(diag(3))
  #NOTE NOTE rbased
  #vectors3d for vectors to be specified as rows of a matrix,
  rownames(vec) <- c("X", "Y", "Z")
  vectors3d(vec, color=c(rep("black",3), lwd=2, radius=1/25))
  planes3d(0, 0, 1, 0, col="gray", alpha=0.2)
  space_cords <- rbind(diag(3))
  e1 <- cbind(c(1,0,0))
  e_bod = t(R %*% vec)
  e_bod_1 = e_bod[1,,drop=FALSE]
  rownames(e_bod_1) = c('e1_bod')
  vectors3d(e_bod_1, lwd=3, col=rep('red',2))
  arrow3d(0.75*e_bod_1, 0.75*e_bod_1 + 0.5* e_bod[2,,drop=FALSE], s=0.2)
  arrow3d(0.75*e_bod_1, 0.75*e_bod_1 + 0.5* e_bod[3,,drop=FALSE], s=0.2)
  rgl.texts(x=0.52,y=0.5,text='Hallo')
}

if (FALSE){
  ## Make the plot a bit larger
  open3d()
  
  #Different Values of last rotation 
  clear3d() #clears Display
  #The last parameter is for the roll 
  show_coordinates(from_fixed_to_body(0,0,0))
  show_coordinates(from_fixed_to_body(0,0,45))
  
  show_coordinates(from_fixed_to_body(10,-60,0))
  show_coordinates(from_fixed_to_body(10,-60,45))
  
  #The second parameter is for the pitch
  #Note that the roll changes
  clear3d()
  show_coordinates(from_fixed_to_body(10,-60,0))
  show_coordinates(from_fixed_to_body(10, 20,45))
  
  #The first paramater is for the yaw
  #Note that the roll changes
  clear3d()
  show_coordinates(from_fixed_to_body(0,-60,0))
  show_coordinates(from_fixed_to_body(45,-60,0))
  show_coordinates(from_fixed_to_body(90,-60,0))
  
  # Determination of the angles from the accelometer
  # In the fixed coordinate system the force goes down the minus -z.
  # F_s = (0,0,-1) in Units of g
  # In bend device the following force is measured
  # F_b = (0.3,0.2,0.5) note that this has to sum up to one. 
  # If we would know a,b,g than with 
  #       R(a,b,g) = from_fixed_to_body(90,-60,0)
  # The following relation would hold.
  #   F_b = R * F_s
  # Estination procedure:
  # F_hat = R(a,b,g) * F_s
  # Minimize mean squared error of 
  # ||F_hat - F_b||^2
  
  F_s = tf$reshape(k_variable(c(0.,0.,1.)), shape=c(3L,1L))
  estimate_par_1 = function(F_b, w){
    for (i in 1:200){
      with(tf$GradientTape() %as% t, {
        R = from_fixed_to_body_tf(w)
        F_hat = tf$matmul(R, F_s)
        loss = tf$reduce_mean(tf$square(F_b - F_hat))
      })
      grad_w = t$gradient(loss, w)
      w$assign(w - 0.1 * grad_w)
      if (i %% 20 == 0) {print(paste0(i, ' ', loss))}
    }
    return(w)
  }
  #estimate_par = tf_function(estimate_par_1)
  F_b = tf$reshape(k_variable(c(0.3,0.2,0.5)), shape=c(3L,1L))
  ws = matrix(0, nrow = 10, ncol = 3)
  for (i in 1:10){
    w =  k_variable(c(runif(3,20,30))*2*pi/360)
    w = estimate_par_1(F_b, w)
    ws[i,] = 360/(2*pi)*w$numpy()
  }
  
}

##### Quaterions helper funcions ####
#from https://automaticaddison.com/how-to-convert-a-quaternion-to-a-rotation-matrix/
quat_to_mat = function(Q) {
  Q = as.matrix(Q)
  # Extract the values from Q
  q0 = Q[1]
  q1 = Q[2]
  q2 = Q[3]
  q3 = Q[4]
  
  # First row of the rotation matrix
  r00 = 2 * (q0 * q0 + q1 * q1) - 1
  r01 = 2 * (q1 * q2 - q0 * q3)
  r02 = 2 * (q1 * q3 + q0 * q2)
  
  # Second row of the rotation matrix
  r10 = 2 * (q1 * q2 + q0 * q3)
  r11 = 2 * (q0 * q0 + q2 * q2) - 1
  r12 = 2 * (q2 * q3 - q0 * q1)
  
  # Third row of the rotation matrix
  r20 = 2 * (q1 * q3 - q0 * q2)
  r21 = 2 * (q2 * q3 + q0 * q1)
  r22 = 2 * (q0 * q0 + q3 * q3) - 1
  
  # 3x3 rotation matrix
  rot_matrix = matrix(c(r00, r01, r02, r10, r11, r12, r20, r21, r22), ncol=3, byrow = TRUE)
  return (rot_matrix)
}
 




