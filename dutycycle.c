
/* 
This program should get started from the command line with 3 arguments. (not programmed yet for all 3)
The arguments are the percentage that the duty cycle of the outputs should work, 
after the zero detection. And so control the power in a 50Hz grid, during 100 half sine cycles.
It writes directly on and off to the 3 GPIO outputs used in the HeatBatt.

Currently only the acceptance of the argument, and the conversion of it to an integer works.
The rest is not programmed yet: The wiringPi.h library is not installed yet.

To compile it is important to include the library wiringPi after having it installed.
The command for the compliation becomes then:
gcc -o dutycycle dutycycle.c  -lwiringPi


*/
#include <wiringPi.h>
#include <stdio.h>
#include <string.h>


int main(int argc, char *argv[])


{

int periods ;	//variable to do define the number of periods (halve sine-cycles). e.g. 100 is during one second.
char text[255] = "wrong command line argument!!!";
int percentage1 = 0;
int percentage2 = 0;
int percentage3 = 0;
int cyclepart;
int how_long_time;
int time_on; // in microseconds!


/* First start reading in all 3 arguments from the command line:
It is the percentage of every output that needs to bee controlled.
*/
strcpy(text ,argv[1]); //Copy the command line argument into the local string
sscanf (text, "%d", &percentage1);	//Convert from string to integer in percentage
printf ("--- %d %% \n", percentage1);

strcpy(text ,argv[2]); //Copy the command line argument into the local string
sscanf (text, "%d", &percentage2);	//Convert from string to integer in percentage
printf ("--- %d %% \n", percentage2);

strcpy(text ,argv[3]); //Copy the command line argument into the local string
sscanf (text, "%d", &percentage3);	//Convert from string to integer in percentage
printf ("--- %d %% \n", percentage3);


wiringPiSetup ( ) ;
pinMode (29, OUTPUT) ;		// Configure GPIO1 as an output
pinMode (26, OUTPUT) ;
pinMode (27, OUTPUT) ;

/*the mainloop for about 100 half sine-cycles, which is corresponding to around 1 second in a 50Hz grid.
*/


for (how_long_time; how_long_time<101; how_long_time++)
	{
	while (!digitalRead(28) ) {delayMicroseconds(10);} //Wait until next zero detection. Becomes high when zero from grid detected
	while (digitalRead(28) )  {delayMicroseconds(10);}//Wait until end of zero detection to start.


        //loop for 10ms for a ONE half cycle of a sine;	
	for (cyclepart=0; cyclepart<101;cyclepart++)
										{

										if (cyclepart < (100-percentage1)){digitalWrite (29, 0); };  	//set the output for the bank1 low
										if (cyclepart < (100-percentage2)){digitalWrite (26, 0) ;};  	//set the output for the bank low
										if (cyclepart < (100-percentage3)){digitalWrite (27, 0) ;};  	//set the output for the bank low

										if (cyclepart >=(100-percentage1)){digitalWrite (29, 1);} ;		//set the output for the bank high
										if (cyclepart >=(100-percentage2)){digitalWrite (26, 1);} ;		//set the output for the bank high
										if (cyclepart >=(100-percentage3)){digitalWrite (27, 1);} ;		//set the output for the bank high


										delayMicroseconds(90);

										}
		digitalWrite (29, 0) ;  	//set the output for the bank low at the end of the cycle
		digitalWrite (26, 0) ;  	//set the output for the bank low at the end of the cycle
		digitalWrite (27, 0) ;  	//set the output for the bank low at the end of the cycle

	}
return 0;
}
