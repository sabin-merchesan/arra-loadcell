/**
 * @file Scale.h
 * @brief Defines a Scale class that manages two adapter objects.
 */

#pragma once

namespace arra {

/**
 * @class Scale
 * @brief Manages two adapter objects to provide calibrated scale readings.
 * 
 * This class takes two adapter objects and provides methods to calibrate and get readings.
 * The readings are averaged from both adapters, and the class provides drift and calibration checks.
 * 
 * @tparam TAdapter The type of adapter. Must have `Calibrate` and `GetValue` methods.
 */
template<class TAdapter>
class Scale 
{

public:
    /**
     * @brief Construct a new Scale object.
     * 
     * @param first The first adapter object.
     * @param second The second adapter object.
     */
    Scale(TAdapter& first, TAdapter& second);

    /**
     * @brief Calibrate both adapter objects.
     * 
     * @param refMass The known mass for calibration.
     */
    void Calibrate(const float refMass);

    /**
     * @brief Get the calibrated value from the scale.
     * 
     * @return float The calibrated value.
     */
    float GetValue() const;

private:
    TAdapter& first_;
    TAdapter& second_;
    
    float measured_;
    float driftReference_;

    static constexpr float driftThreshold_  = 0.5;
    static constexpr float calibThreshold_  = 0.3;
};

} // namespace arra
