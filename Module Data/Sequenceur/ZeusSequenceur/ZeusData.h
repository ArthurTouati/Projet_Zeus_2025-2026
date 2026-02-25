#ifndef ZEUS_DATA_H
#define ZEUS_DATA_H

typedef struct struct_data {
  int id_card;            // unique value for each ESP-32 (1 for Sequenceur, 2 for Data, 3 for Payload)
  float time_for_apogee;  // time for apogee (to calculate for the parachute)
  bool launch;            // Launch is done or not (detect by the Sequenceur)
  unsigned long timestamp;// Obtain timestamp for every steps
} struct_data;

#endif