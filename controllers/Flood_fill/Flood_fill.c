/*
 * File:          
 * Date:
 * Description:
 * Author: Sebastian Sosnowski
 * Modifications:
 */

#include <stdio.h>
#include <webots/robot.h>
#include <webots/distance_sensor.h>
#include <webots/motor.h>
#include <math.h>
#include <webots/position_sensor.h>
#include <webots/keyboard.h>
#include <stdlib.h>

#define TIME_STEP 64
#define TILE 0.12 //tile length
#define AXLE 0.0568 //axle length 0.0568
#define WHEEL 0.02002 //wheel radius 0.02002
#define SPEED 2

//Walls values according to global direction (NORTH is not always forward etc.)
#define  WEST    1    //  00000001 
#define  SOUTH   2    //  00000010 
#define  EAST    4    //  00000100 
#define  NORTH   8    //  00001000

#define ROWS 16
#define COLUMNS 16
#define MAZE_SIZE ROWS * COLUMNS //16x16
#define VISITED 64
#define MODE 2 // 1- keyboard, 2- search, 3 - speeedrun

//Sets correct target for used mode
#if MODE == 3
  #define TARGET_CELL 136
#elif MODE == 2
  #define TARGET_CELL 1
#else 
  #define TARGET_CELL 0
#endif

  
              /* START Map updating functions */
              
void add_wall(unsigned char map[],unsigned char position, char orientation, unsigned char Wall);              
void init_map(unsigned char map[]);
void init_dist(unsigned char dist[], unsigned char target);

              /* END Map updating functions */
              
              /* START Algorythm related functions */ 
                                         
char change_orientation(char orientation, char action);
unsigned char change_position(unsigned char position, char orientation);
void floodfill(unsigned char map[], unsigned char current_position, unsigned char distance[]);  
unsigned char where_to_move(unsigned char map[], unsigned char current_position, unsigned char distance[], unsigned char orientation);
unsigned char change_target( unsigned char map[], unsigned char position, unsigned char target, unsigned char distance[]);

              /* END Algorythm related functions */ 
              
              /* START Move related functions */

void move_1_tile(WbDeviceTag left_motor, WbDeviceTag right_motor, WbDeviceTag ps_left, WbDeviceTag ps_right);
void turn(char key, WbDeviceTag left_motor, WbDeviceTag right_motor, WbDeviceTag ps_left, WbDeviceTag ps_right);
void wait_move_end(WbDeviceTag ps_left, WbDeviceTag ps_right);
void speed_correction(double left_wall, double right_wall, WbDeviceTag left_motor, WbDeviceTag right_motor);

              /* END Move related functions */
              
              /* START Other functions */
              
void print_array(unsigned char map[],int action);

              /* END Other functions */

int main(int argc, char **argv) {
  /* necessary to initialize webots stuff */
  wb_robot_init();
  
  unsigned char map[MAZE_SIZE] = 
  {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  
  unsigned char distance[MAZE_SIZE];
  
  unsigned char position = 0;
  unsigned char direction = 8; //where robot wants to move
  unsigned char target = TARGET_CELL;
  char key;
  char mode = MODE; // 1- keyboard, 2- search, 3 - speeedrun
  int open = 1; //to open file 1 time
  init_map(map);

  char orientation = NORTH; //orientation of the robot
  
  //enable distance sensors
  WbDeviceTag ps[8]; // 8 sensors
  char ps_names[8][4] = {
  "ps0", "ps1", "ps2", "ps3",
  "ps4", "ps5", "ps6", "ps7"
  };
  
  
  for (int i = 0; i < 8 ; i++)
  {
    ps[i] = wb_robot_get_device(ps_names[i]);
    wb_distance_sensor_enable(ps[i], TIME_STEP);
  }
  WbDeviceTag left_motor = wb_robot_get_device("left wheel motor");
  WbDeviceTag right_motor = wb_robot_get_device("right wheel motor");
  
  WbDeviceTag ps_left = wb_robot_get_device("left wheel sensor");
  WbDeviceTag ps_right = wb_robot_get_device("right wheel sensor");
  wb_position_sensor_enable(ps_left, TIME_STEP);
  wb_position_sensor_enable(ps_right, TIME_STEP);
  
      
  //get key presses from keyboard 
  wb_keyboard_enable(TIME_STEP);
  
  //basic velocity
  wb_motor_set_velocity(left_motor,SPEED);
  wb_motor_set_velocity(right_motor,SPEED);

                              /* MAIN LOOP */
      /****************************************************************/
      /****************************************************************/
      /****************************************************************/
      
      
  while (wb_robot_step(TIME_STEP) != -1) {
           
   double avg_2 = 0; //right sensor
   double avg_4 = 0; //back sensor
   double avg_5 = 0; //left sensor
   double avg_7 = 0; //front sensor
   double n = 5;
 
   //read distance sensors
   double ps_values[8];
    
   for(int i = 0; i < 5; i++) //5 scans for better accuracy
   {
     for(int i = 0; i<8; i++)
     {
       ps_values[i] = wb_distance_sensor_get_value(ps[i]); 
     }    
     avg_2 += ps_values[2];

     avg_4 += ps_values[4];

     avg_5 += ps_values[5];

     avg_7 += ps_values[7];
        
     wb_robot_step(TIME_STEP); //for simulation to update data
   }
   //average score of sensors measurement
   avg_2 = avg_2 / n;
   avg_4 = avg_4 / n;
   avg_5 = avg_5 / n;
   avg_7 = avg_7 / n;   
   
    /* START Wall detection */
       
     bool left_wall = avg_5 > 80.0;
     bool front_wall = avg_7 > 80.0;
     bool right_wall = avg_2 > 80.0;
     bool back_wall = avg_4 > 80.0;
     
     if(left_wall)  add_wall(map, position, orientation, WEST);
     if(front_wall) add_wall(map, position, orientation, NORTH);
     if(right_wall) add_wall(map, position, orientation, EAST);
     if(back_wall)  add_wall(map, position, orientation, SOUTH);
     
        /* END Wall detection */
        
  if(mode == 1)
  {
        /* START Robot control with keyboard */
    
    switch(key = wb_keyboard_get_key())
    {
      case 'W':   //go up
        move_1_tile(left_motor,right_motor, ps_left, ps_right);
        break;
            
      case 'D': //turn right
      case 'A': //turn left
        turn(key, left_motor, right_motor, ps_left, ps_right);
        break;
      case 'S':
        break;
    }
  
        /* END Robot control with keyboard */ 
    }
   else if(mode == 2)
   {
              /* START floodfill search run */
        
  //print map with explored walls  
  printf("MAPA \n"); 
  print_array(map, 0); 
  printf("MAPA \n"); 
  
  init_dist(distance, target); //reset path
  floodfill(map, 0, distance); //path
  direction = where_to_move(map, position, distance, orientation);
  
  
  if(orientation == direction) //forward
  {
    if(left_wall && right_wall) speed_correction(avg_5, avg_2, left_motor, right_motor);
    move_1_tile(left_motor,right_motor, ps_left, ps_right);
  }
  else if( !((orientation == WEST) && (direction == NORTH)) != !( (orientation / 2) == direction) ) //right, XOR, '!' to avoid nonzero values
  {
   orientation = change_orientation(orientation, 'D');
   turn('D', left_motor, right_motor, ps_left, ps_right);
   move_1_tile(left_motor,right_motor, ps_left, ps_right);
  }
  else if( !((orientation == NORTH) && (direction == WEST)) != !( (orientation * 2) == direction) ) //left, XOR
  {
    orientation = change_orientation(orientation, 'A');
    turn('A', left_motor, right_motor, ps_left, ps_right);
    move_1_tile(left_motor,right_motor, ps_left, ps_right);
  }
  else if( !( (orientation * 4) == direction) != !( (orientation / 4) == direction) ) //back, XOR
  {
    orientation = change_orientation(orientation, 'S');
    turn('S', left_motor, right_motor, ps_left, ps_right);
    move_1_tile(left_motor,right_motor, ps_left, ps_right);
  }
   
             
   position = change_position(position, orientation); 
   map[position] = map[position] | VISITED; //mark visited tile
   
   if(position == target)
   {
     target = change_target(map, position, target, distance);
   }
   
              /* END floodfill search run */
   }
   else if(mode == 3)
   {
              /* START floodfill fast run */
     if(open)
     {
       FILE *trasa;
       trasa = fopen("trasa.txt","rb");
       if(trasa == NULL)
       {
         printf("ERROR \n");
         exit(1);
       }
       fread(distance,sizeof(unsigned char),MAZE_SIZE,trasa);
       fclose(trasa);
       print_array(distance, 0);
       
       FILE *mapa;
       mapa = fopen("mapa.txt","rb");
       if(mapa == NULL)
       {
         printf("ERROR \n");
         exit(1);
       }
       fread(map,sizeof(unsigned char),MAZE_SIZE,mapa);
       fclose(mapa);
       print_array(map, 1);
       
       open = 0;
     }
     
       //floodfill(map, 0, distance); //path
       direction = where_to_move(map, position, distance, orientation);
  
  
      if(orientation == direction) //forward
      {
        if(left_wall && right_wall) speed_correction(avg_5, avg_2, left_motor, right_motor);
        move_1_tile(left_motor,right_motor, ps_left, ps_right);
      }
      else if( !((orientation == WEST) && (direction == NORTH)) != !( (orientation / 2) == direction) ) //right, XOR, '!' to avoid nonzero values
      {
       orientation = change_orientation(orientation, 'D');
       turn('D', left_motor, right_motor, ps_left, ps_right);
       move_1_tile(left_motor,right_motor, ps_left, ps_right);
      }
      else if( !((orientation == NORTH) && (direction == WEST)) != !( (orientation * 2) == direction) ) //left, XOR
      {
        orientation = change_orientation(orientation, 'A');
        turn('A', left_motor, right_motor, ps_left, ps_right);
        move_1_tile(left_motor,right_motor, ps_left, ps_right);
      }
      else if( !( (orientation * 4) == direction) != !( (orientation / 4) == direction) ) //back, XOR
      {
        orientation = change_orientation(orientation, 'S');
        turn('S', left_motor, right_motor, ps_left, ps_right);
        move_1_tile(left_motor,right_motor, ps_left, ps_right);
      }
                 
       position = change_position(position, orientation); 
       
       if(position == target)
       {
         printf("koniec\n");
         wb_robot_cleanup();
         exit(0);
       }
              /* END floodfill fast run */
   }
   
  }

  wb_robot_cleanup();

  return 0;
}



























                              /* FUNCTIONS */
      /****************************************************************/
      /****************************************************************/
      /****************************************************************/


                    /* START Move related functions */
// makes robot to move 1 tile
void move_1_tile(WbDeviceTag left_motor, WbDeviceTag right_motor, WbDeviceTag ps_left, WbDeviceTag ps_right)
{
   double revolution_l, revolution_r, rev;
  
  rev = TILE/WHEEL; //how many rev in radians
  revolution_l = wb_position_sensor_get_value(ps_left);
  revolution_r = wb_position_sensor_get_value(ps_right);
  revolution_l += rev;
  revolution_r += rev;
  wb_motor_set_position(left_motor, revolution_l);
  wb_motor_set_position(right_motor, revolution_r);
  printf("prosto \n");
  wait_move_end(ps_left, ps_right);
}

// makes robot to turn
void turn(char key, WbDeviceTag left_motor, WbDeviceTag right_motor, WbDeviceTag ps_left, WbDeviceTag ps_right)
{
  double revolution_l, revolution_r, rev;
  
  rev = (M_PI/2) * AXLE/2/WHEEL; //how many rev in radians
  
  revolution_l = wb_position_sensor_get_value(ps_left);
  revolution_r = wb_position_sensor_get_value(ps_right);
  
  wb_motor_set_velocity(right_motor,SPEED);
  wb_motor_set_velocity(left_motor,SPEED);
  
  switch(key)
  {
    case 'D':
    revolution_l += rev;
    revolution_r -= rev;
    wb_motor_set_position(left_motor, revolution_l);
    wb_motor_set_position(right_motor, revolution_r);
    printf("prawo \n");
    break;
    case 'A':
    revolution_l -= rev;
    revolution_r += rev;
    wb_motor_set_position(left_motor, revolution_l);
    wb_motor_set_position(right_motor, revolution_r);
    printf("lewo \n");
    break;
    case 'S':
    rev = M_PI * AXLE/2/WHEEL;
    revolution_l += rev;
    revolution_r -= rev;
    wb_motor_set_position(left_motor, revolution_l);
    wb_motor_set_position(right_motor, revolution_r);
    printf("tyl \n");
    break;
  }
  wait_move_end(ps_left, ps_right);
}

//checks when robots stops moving (to not allow sensors to scan)
void wait_move_end(WbDeviceTag ps_left, WbDeviceTag ps_right)
{
double dist_left, dist_left_2, dist_right, dist_right_2;
 
  do
     { 
       dist_left = wb_position_sensor_get_value(ps_left); 
       dist_right = wb_position_sensor_get_value(ps_right);
       wb_robot_step(TIME_STEP);
       dist_left_2 = wb_position_sensor_get_value(ps_left);
       dist_right_2 = wb_position_sensor_get_value(ps_right);
         
     }while((dist_left != dist_left_2) && (dist_right != dist_right_2) );
}

//correct robot position according to distance sensors by changing motors speed
void speed_correction(double left_wall, double right_wall, WbDeviceTag left_motor, WbDeviceTag right_motor)
{
  if(fabs(left_wall - right_wall) > 20)
       {
         if(left_wall > right_wall) 
         {
           wb_motor_set_velocity(right_motor,SPEED * 0.96);
           wb_motor_set_velocity(left_motor,SPEED);
         }
         else 
         {
           wb_motor_set_velocity(right_motor,SPEED);
           wb_motor_set_velocity(left_motor,SPEED * 0.96);
         }
       }
  else if(fabs(left_wall - right_wall) > 10)
       {
         if(left_wall > right_wall) 
         {
           wb_motor_set_velocity(right_motor,SPEED * 0.98);
           wb_motor_set_velocity(left_motor,SPEED);
         }
         else 
         {
           wb_motor_set_velocity(right_motor,SPEED);
           wb_motor_set_velocity(left_motor,SPEED * 0.98);
         }
       }
}
                    /* END Move related functions */
                    
                    /* START Map updating functions */
                    
//add wall according to distance sensors
void add_wall(unsigned char map[],unsigned char position, char orientation, unsigned char Wall)
{
  if(orientation == EAST)
  {
    if(Wall != WEST) Wall /= 2;
    else Wall = 8;
  }
  else if(orientation == SOUTH)
  {
    if( (Wall == WEST) || (Wall == SOUTH) ) Wall *= 4;
    else Wall /= 4;
  }
  else if(orientation == WEST)
  {
    if(Wall != NORTH) Wall *= 2;
    else Wall = 1;
  }
  
  
  map[position] = map[position] | Wall; //adds sensed wall
  
  if( Wall == NORTH ) 
  { 
    position = position + COLUMNS;          //upper field
    map[position] = map[position] | SOUTH; 
  } 
  if( Wall == EAST ) 
  { 
    position = position + 1; 
    map[position] = map[position] | WEST; //field on the left
  } 
  if( Wall == SOUTH ) 
  { 
    position = position - COLUMNS;   
    map[position] = map[position] | NORTH;  //lower field
  } 
  if( Wall == WEST ) 
  { 
  position = position - 1;   
  map[position] = map[position] | EAST; //field on the rught
  } 
}

//init maze map with external walls
void init_map(unsigned char map[])
{
  map[0] = map[0] | VISITED; //mark start as visited
  
  for(int i = 0; i < 16 ;i++)
  {
    map[i] = map[i] | SOUTH;
  }
  for(int i = 240; i < 256 ;i++)
  {
   map[i] = map[i] | NORTH;
  }
  for(int i = 0; i < 241 ;i+=16)
  {
   map[i] = map[i] | WEST;
  }
  for(int i = 15; i < 256 ;i+=16)
  {
   map[i] = map[i] | EAST;
  }
  
  print_array(map, 0);
  
}

//init distance map with 255 and 0 as target (needed for floodfill algorythm)
void init_dist(unsigned char dist[], unsigned char target)
{
  for(int i = 0; i < MAZE_SIZE; i++)
  {
    dist[i] = 255;
  }
  dist[target] = 0;
}

                    /* END Map updating functions */

                    /* START Algorythm related functions */ 
                    
//change robot orientation basing on last orientation and last turn
char change_orientation(char orientation, char action)
{
  switch(action)
  {
    case 'D': //turning right
      if(orientation == WEST) orientation = NORTH; 
      else orientation = orientation / 2;
      break;
    case 'A': //turning left
      if(orientation == NORTH) orientation = WEST; 
      else orientation = orientation * 2;
      break;
    case 'S': //turning back
      if((orientation == NORTH) || (orientation == EAST)) orientation = orientation / 4; 
      else orientation = orientation * 4;
      break;
  }
  printf("orientacja: %d \n", orientation);
  return orientation;
} 
                   
//update position of the robot basing on current orientation of the robot
unsigned char change_position(unsigned char position, char orientation)
{
  if( orientation == NORTH ) 
  { 
    position = position + COLUMNS;          
  } 
  if( orientation == EAST ) 
  { 
    position = position + 1; 
  } 
  if( orientation == SOUTH ) 
  { 
    position = position - COLUMNS;    
  } 
  if( orientation == WEST ) 
  { 
    position = position - 1;    
  } 
  
  
   return position;
}

//floodfill algorythm
void floodfill(unsigned char map[], unsigned char current_position, unsigned char distance[])
{
bool search = true;
while(search) 
{
  search = false;
  for(int i = 0; i < MAZE_SIZE; i++)
  {
    if(distance[i] < 255)
    {
      if((map[i] & NORTH) != NORTH)
      {
        //if(distance[i + COLUMNS] == 255)
        if(distance[i + COLUMNS] == 255 || ((distance[i] +1) < distance[i + COLUMNS])) 
        {
          distance[i + COLUMNS] = distance[i] + 1; //NORTH 
          search = true;
        }  
      }
      if((map[i] & EAST) != EAST)
      {
        if(distance[i + 1] == 255 || ((distance[i] +1) < distance[i + 1])) 
        {
          distance[i + 1] = distance[i] + 1; //EAST
          search = true;
        }
      }
      if((map[i] & SOUTH) != SOUTH)
      {
        if(distance[i - COLUMNS] == 255 || ((distance[i] +1) < distance[i - COLUMNS])) 
        {
          distance[i - COLUMNS] = distance[i] + 1; //SOUTH
          search = true;
        }
      }
      if((map[i] & WEST) != WEST)
      {
        if(distance[i - 1] == 255 || ((distance[i] +1) < distance[i - 1]))  
        {
          distance[i - 1] = distance[i] + 1; //WEST
          search = true;
        }
      }
    } 
  }
}
  
printf("\n TRASA \n");
print_array(distance, 0);
printf("\n TRASA \n");

}

//decide where to move by checking distance values in neighbors cells
unsigned char where_to_move(unsigned char map[], unsigned char current_position, unsigned char distance[], unsigned char orientation)
{
  unsigned char best_neighbor = 255;
  unsigned char direction = NORTH;
  
      if((map[current_position] & NORTH) != NORTH)
      {
        if(distance[current_position + COLUMNS] <= best_neighbor) 
        {
          if(distance[current_position + COLUMNS] < best_neighbor)
          {
            best_neighbor = distance[current_position + COLUMNS];
            direction = NORTH; 
          }
          else if(orientation == NORTH) direction = NORTH;
        }  
      }
      if((map[current_position] & EAST) != EAST)
      {
        if(distance[current_position + 1] <= best_neighbor) 
        {
          if(distance[current_position + 1] < best_neighbor)
          {
            best_neighbor = distance[current_position + 1];
            direction = EAST;
          }
          else if(orientation == EAST) direction = EAST;
        }
      }
      if((map[current_position] & SOUTH) != SOUTH)
      {
        if(distance[current_position - COLUMNS] <= best_neighbor) 
        {
        if(distance[current_position - COLUMNS] < best_neighbor)
        {
          best_neighbor = distance[current_position - COLUMNS];
          direction = SOUTH;
        }
        else if(orientation == SOUTH) direction = SOUTH;
        }
      }
      if((map[current_position] & WEST) != WEST)
      {
        if(distance[current_position - 1] <= best_neighbor)  
        {
          if(distance[current_position - 1] < best_neighbor)
          {
          best_neighbor = distance[current_position - 1];
          direction = WEST;
          }
          else if(orientation == WEST) direction = WEST;
        }
      }
      
      return direction;
}

//marks every visited cell, after reaching targeted cell, change cell to first unvisited cell
//when reaching final target, saves distance map to file
unsigned char change_target( unsigned char map[], unsigned char position, unsigned char target, unsigned char distance[])
{
     bool search = true;
     int i = 0;
     
     while(search) //search to find unvisited cell, otherwise end
     {
       if( !(map[i] & VISITED) ) 
       {
         target = i;
         search = false;
         printf("target = %d\n",target);
       }
       else i++;
       if(i == 256) //if all cells visited, go to final target
       {
         target = 136;
         printf("target = %d\n",target);
         search = false;
         i = 0;
       }
       
     }
     if((position == target) && (i == 0) && (target == 136)) //after reaching final target, save result in file
     {
       printf(" KONIEC!!!!!!!!! \n");
       FILE *trasa;
       trasa = fopen("trasa.txt","wb");
       if(trasa == NULL)
       {
         printf("ERROR \n");
         exit(1);
       }
       fwrite(distance,sizeof(unsigned char),MAZE_SIZE,trasa);
       fclose(trasa);
       trasa = fopen("trasa.txt","rb");
       if(trasa == NULL)
       {
         printf("ERROR \n");
         exit(1);
       }
       fread(distance,sizeof(unsigned char),MAZE_SIZE,trasa);
       fclose(trasa);
       print_array(distance, 0);
       
       FILE *mapa;
       mapa = fopen("mapa.txt","wb");
       if(mapa == NULL)
       {
         printf("ERROR \n");
         exit(1);
       }
       fwrite(map,sizeof(unsigned char),MAZE_SIZE,mapa);
       fclose(mapa);
       mapa = fopen("mapa.txt","rb");
       if(mapa == NULL)
       {
         printf("ERROR \n");
         exit(1);
       }
       fread(map,sizeof(unsigned char),MAZE_SIZE,mapa);
       fclose(mapa);
       print_array(map, 1);
       wb_robot_cleanup();
       exit(0);
     } 
     
     /*  
     if(target == 136) target = 120;
     else if(target == 120) target = 119;
     else if(target == 119) target = 135;
     else
     {
     printf(" KONIEC!!!!!!!!! \n");
     mode = 1;
     }
   */
   
   return target;  
}

                    /* END Algorythm related functions */

                    /* START Other functions */ 
                                        
//print array in a shape of maze (16x16 etc.)    
void print_array(unsigned char map[],int action)
{
  printf(" \n");
  if(action == 0) //just print array
  {
    for(int i = 240, k = 1; i >= 0; i++)
     {
       printf("%3d ",map[i]);
       if(k == 16)
       {
         printf("\n");
         i-=32;
         k = 1;
       }
       else k++;
     }
   }
   else if(action == 1) //print array without visited mark to read just walls
   {
     unsigned char array[MAZE_SIZE];
     
     for(int i = 0; i <= 255; i++) 
     {
       array[i] = map[i];
       array[i] -= 64; //version to avoid negative values(errors etc.)  if(array[i] & VISITED) array[i] -= 64;
     }
     for(int i = 240, k = 1; i >= 0; i++)
     {
       printf("%3d ",array[i]);
       if(k == 16)
       {
         printf("\n");
         i-=32;
         k = 1;
       }
       else k++;
     }
   }
   printf(" \n");  
}
                    /* END Other functions */
