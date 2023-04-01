/*
 * File:          Maze_moving_PID.c
 * Date:
 * Description:
 * Author:
 * Modifications:
 */

#include <stdio.h>
#include <stdlib.h>

#include <webots/robot.h>
#include <webots/distance_sensor.h>
#include <webots/motor.h>

#define TIME_STEP 64
#define MAX_SPEED 6.28

void SetSpeed(double ls, double rs, double balance);
double pid(double error);


int main(int argc, char **argv) {
  /* necessary to initialize webots stuff */
  wb_robot_init();
  
  
  //enable distance sensors
  int i;
  WbDeviceTag ps[8]; // 8 sensors
  char ps_names[8][4] = {
  "ps0", "ps1", "ps2", "ps3",
  "ps4", "ps5", "ps6", "ps7"
  };
  
  for (i = 0; i<8 ; i++)
  {
    ps[i] = wb_robot_get_device(ps_names[i]);
    wb_distance_sensor_enable(ps[i], TIME_STEP);
  }
  WbDeviceTag left_motor = wb_robot_get_device("left wheel motor");
  WbDeviceTag right_motor = wb_robot_get_device("right wheel motor");
  wb_motor_set_position(left_motor, INFINITY);
  wb_motor_set_position(right_motor, INFINITY);
  wb_motor_set_velocity(left_motor, 0.0);
  wb_motor_set_velocity(right_motor, 0.0);
 
   //ini motors 50% speed
   double ls = 0.5 * MAX_SPEED;
   double rs = 0.5 * MAX_SPEED;
     
   double error,last_error, I, D, P;
   error = last_error = I = D = P = 0;
   double pid_result = 0;
   
   double kp, ki, kd;
   kp = 0.005;
   ki = 0;
   kd = 0.15;
   
   
  while (wb_robot_step(TIME_STEP) != -1) {
  
                  
    //read sensors
    double ps_values[8];
    for(int i = 0; i<8; i++)
    {
      ps_values[i] = wb_distance_sensor_get_value(ps[i]);
    }
      
    printf("ps_values[1] = %f \n", ps_values[1]);
    printf("ps_values[6] = %f \n", ps_values[6]);
    
    if(abs(ps_values[6] - ps_values[1]) > 50)
    {
      error = ps_values[6] - ps_values[1];
      //pid_result = pid(error);
      //pid
      P = error;
      I = error + I;
      D = error - last_error;
      pid_result = kp * P + ki * I + kd * D;
      last_error = error;
      
      
    }
    //SetSpeed(ls, rs, pid_result);
    if(abs(ls + pid_result) > 6.28) ls = MAX_SPEED;
    else ls = ls + pid_result;
    
    if(abs(rs - pid_result) > 6.28) rs = MAX_SPEED;
    else rs = rs - pid_result;
    
    wb_motor_set_velocity(left_motor, ls);
    wb_motor_set_velocity(right_motor, rs);
  }

 
  wb_robot_cleanup();

  return 0;
}
/*
void SetSpeed(double ls, double rs, double balance)
{
  wb_motor_set_velocity(left_motor, ls + balance);
  wb_motor_set_velocity(right_motor, rs - balance);
}

double pid(double error)
{
  double balance;
  P = error;
  I = error + I;
  D = error - last_error;
  balance = kp * P + ki * I + kd * D;
  last_error = error;
  return balance;
} 
*/
