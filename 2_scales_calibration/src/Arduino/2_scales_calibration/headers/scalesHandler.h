#pragma once
#include "scale.h"
#include "proto.h"

namespace  arra {

    class Scales {   
        public:
            Scales() : nr_scales_(0) {}

            void Calibrate(const byte* buffer) {
                const int id = static_cast<int>(buffer[1]);
                if (isNotValidIndex(id)) {
                    return;
                }
                scales_[id].Calibrate();
            }

            void Config(const byte* buffer) {           
                Message message;
                decode_config_command(buffer, message);
                const int id = message.config.scaleIndex;
                if (isNotValidIndex(id)) {
                    return;
                }
                scale_config config;
                config.calibrationMass = message.config.calibrationMass;
                config.numReadings = message.config.numReadings;
                scales_[id].Config(config);
            }

            void AddScale(const int pinOut, const int pinSck, const int id) {
                scales_[id] = Scale(pinOut, pinSck);
                nr_scales_++;                
            }   

            float GetValueFromIndex(const int index) {
                if (isNotValidIndex(index)) {
                    return 0.0f;
                }
                return scales_[index].GetValue();
            }   

            Message getWeightMessage() {
                Message message;
                message.weight.numberOfScales = nr_scales_;
                for (int i = 0; i < nr_scales_; i++) {
                    message.weight.floatWeight[i] = GetValueFromIndex(i);
                }
                return message;
            }

            


                          

        private:
            Scale scales_[15];
            int nr_scales_;

            bool isNotValidIndex(const int index) {
                return index < 0 || index >= nr_scales_;
            }   
    };
}