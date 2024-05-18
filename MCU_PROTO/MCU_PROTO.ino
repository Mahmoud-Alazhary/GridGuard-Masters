//power in W,arduino digital pins from 0 to 3
byte nl=4;
//sorted by priority
int loads[4]={5,3,1,9};
//reactive power in kvar
int reactive_power_loads[4]={50,30,0,1};
//sorted in decendings
int generators_capacity[3]={100,100,100};
int total_cap=0,total_loads=0,total_reactive=0;
int loads_mask=0,generators_mask=1;
int step_Q[6] = {5000, 15000, 9000, 10000, 20000, 8000};
static const uint8_t analog_pins[] = {A0,A1,A2,A3};
//from 0 to 3 ==>load state reading
//from 4 to 7 load out
//from 8 to 10 gen in
//from 11 to 13 gen out
/*
    check if new load connected 

*/
byte find_mask(float Q_comp){
        float mn = 1e9;
        byte best_mask = 0, ans_cnt = 0;
        for (int msk = 0; msk < 16; msk++)//2^4
        {
            float tmp_sum = 0;
            byte cnt = 0;
            for (byte d = 0; d < 6; d++)
            {
                if ((msk & (1 << d)))
                {

                    cnt++;
                    tmp_sum += step_Q[d];
                }
            }
            if (tmp_sum > Q_comp)
                continue; // invalid mask
            // get best mask
            if (Q_comp - tmp_sum < mn || (Q_comp - tmp_sum == mn && cnt < ans_cnt))
            {
                ans_cnt = cnt;
                mn = Q_comp - tmp_sum;
                best_mask = msk;
            }
        }
        Serial.print("Q_comp: ");
        Serial.println(Q_comp);
        Serial.print("Best Mask: ");
        Serial.println(best_mask);
        return best_mask;
}
void reset(){
    for(byte i=4;i<=7;i++)digitalWrite(i,LOW);
    for(byte i=11;i<=13;i++)digitalWrite(i,LOW);
    digitalWrite(11,HIGH);
    total_loads=0;
    total_reactive=0;
    
}
void process(){
    reset();
    int cur_cap=generators_capacity[0];
    total_loads=0;
    total_reactive=0;
    byte ptr=1;
    for(int i=0;i<4;i++){
        if(loads[i]){
            total_loads+=loads[i];
            total_reactive+=reactive_power_loads[i];
            
            digitalWrite(4+i,HIGH);
            if(i==0)
              delay(5000);
        }
        while(cur_cap<total_loads&&ptr<3){
            cur_cap+=generators_capacity[ptr];
            digitalWrite(ptr+11,HIGH);
            delay(20000);
            ptr++;
            
        }
        
    }
        Serial.print("=> ");Serial.println(ptr);
        byte ptr2=3;
        while(cur_cap<total_loads){//can't supply all of that, cut off few loads
            total_loads-=loads[ptr2];
            total_reactive-=reactive_power_loads[ptr2];
            digitalWrite(ptr2+4,LOW);
            ptr2--;
            delay(30000);
        }
        
        //remove extra generators..
        while(cur_cap-generators_capacity[ptr-1]>total_loads&&ptr>1){
            ptr--;
            cur_cap-=generators_capacity[ptr];
            digitalWrite(ptr+11,LOW);
        }
        
        //now calc best mask
        byte mask=find_mask(total_reactive);
        //applying mask
        for(int i=0;i<4;i++){
            if(mask&(1<<i)){
                digitalWrite(analog_pins[i],HIGH);
            }
            else{
                digitalWrite(analog_pins[i],LOW);
            }
        }
        
        Serial.print(ptr);
        Serial.print(" ");
        Serial.println(ptr2);
}
void setup() {
  Serial.println("Grid Gaurd LOGGER");
    for(byte i=0;i<=3;i++)pinMode(i,INPUT);
    for(byte i=4;i<=7;i++)pinMode(i,OUTPUT);
    for(byte i=8;i<=10;i++)pinMode(i, INPUT);
    for(byte i=11;i<=13;i++)pinMode(i,OUTPUT);
    Serial.begin(9600);
    //first generator is always turned on
    digitalWrite(11,HIGH);
    total_cap+=generators_capacity[0];
    
    //loads[4]={100,100,100,100};
    loads[0]=100;loads[1]=100;loads[2]=100;loads[3]=100;
    //reactive_power_loads[4]={50,30,0,1};
    reactive_power_loads[0]=50;reactive_power_loads[1]=30;reactive_power_loads[2]=10;reactive_power_loads[3]=1;
    Serial.println("Running Case 1..");
    process();
    Serial.println("Waitting..");
    delay(7000);
    
}

void loop() {
  // read load states
    
}
