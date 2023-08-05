/*
 * Copyright (c) 2018-2020 REV Robotics
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of REV Robotics nor the names of its
 *    contributors may be used to endorse or promote products derived from
 *    this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#pragma once

#include "rev/CANError.h"
#include "rev/CANSensor.h"

#include <stdint.h>

#include <atomic>

namespace rev {

class CANSparkMax;

class CANEncoder: public CANSensor {
public:

    enum class EncoderType {
        kNoSensor = 0,
        kHallSensor = 1,
        kQuadrature = 2,
        kSensorless = 3
    };

    enum class AlternateEncoderType {
        kQuadrature
    };

    /**
     * Constructs a CANEncoder.
     *
     * @param device The Spark Max to which the encoder is attached.
     * @param sensorType The encoder type for the motor: kHallEffect or kQuadrature
     * @param counts_per_rev The counts per revolution of the encoder
     */
    explicit CANEncoder(CANSparkMax& device, EncoderType sensorType = CANEncoder::EncoderType::kHallSensor, int counts_per_rev = 42);

    /**
     * Constructs a CANEncoder from the alternate encoder port
     *
     * @param device The Spark Max to which the encoder is attached.
     * @param sensorType The alternate encoder type for the motor: kQuadrature
     * @param counts_per_rev The counts per revolution of the encoder
     */
    explicit CANEncoder(CANSparkMax& device, AlternateEncoderType sensorType, int counts_per_rev);

    CANEncoder(CANEncoder&& rhs);
    CANEncoder& operator=(CANEncoder&& rhs);

    CANEncoder(const CANEncoder& rhs);

    /**
     * Get the position of the motor. This returns the native units
     * of 'rotations' by default, and can be changed by a scale factor
     * using setPositionConversionFactor().
     *
     * @return Number of rotations of the motor
     *
     */
    double GetPosition();

    /**
     * Get the velocity of the motor. This returns the native units
     * of 'RPM' by default, and can be changed by a scale factor
     * using setVelocityConversionFactor().
     *
     * @return Number the RPM of the motor
     *
     */
    double GetVelocity();

    /**
     * Set the position of the encoder.
     *
     * @param position Number of rotations of the motor
     *
     * @return CANError Set to CANError.kOK if successful
     */
    CANError SetPosition(double position);

    /**
     * Set the conversion factor for position of the encoder. Multiplied by the
     * native output units to give you position
     *
     * @param factor The conversion factor to multiply the native units by
     *
     * @return CANError Set to CANError.kOK if successful
     */
    CANError SetPositionConversionFactor(double factor);

    /**
     * Set the conversion factor for velocity of the encoder. Multiplied by the
     * native output units to give you velocity
     *
     * @param factor The conversion factor to multiply the native units by
     *
     * @return CANError Set to CANError.kOK if successful
     */
    CANError SetVelocityConversionFactor(double factor);

    /**
     * Get the conversion factor for position of the encoder. Multiplied by the
     * native output units to give you position
     *
     * @return The conversion factor for position
     */
    double GetPositionConversionFactor();

    /**
     * Get the conversion factor for velocity of the encoder. Multiplied by the
     * native output units to give you velocity
     *
     * @return The conversion factor for velocity
     */
    double GetVelocityConversionFactor();
    
    /**
     * Set the average sampling depth for a quadrature encoder. This value
     * sets the number of samples in the average for velocity readings. This
     * can be any value from 1 to 64.
     * 
     * When the SparkMax controller is in Brushless mode, this 
     * will not change any behavior.
     * 
     * @param depth The average sampling depth between 1 and 64 (default)
     * 
     * @return CANError.kOK if successful
     */
    CANError SetAverageDepth(uint32_t depth);

    /**
     * Set the measurement period for velocity measurements of a quadrature encoder.
     * When the SparkMax controller is in Brushless mode, this will not
     * change any behavior.
     * 
     * The basic formula to calculate velocity is change in positon / change in time.
     * This parameter sets the change in time for measurement.
     * 
     * @param period_us Measurement period in milliseconds. This number may be
     * between 1 and 100 (default).
     * 
     * @return CANError.kOK if successful
     */
    CANError SetMeasurementPeriod(uint32_t period_ms);

    /**
     * Get the averafe sampling depth for a quadrature encoder. 
     * 
     * @return The average sampling depth
     */
    uint32_t GetAverageDepth();

    /**
     * Get the number of samples for reading from a quadrature encoder. This value
     * sets the number of samples in the average for velocity readings.
     * 
     * @return Measurement period in microseconds
     */ 
    uint32_t GetMeasurementPeriod();

    /**
     * Get the counts per revolution of the quadrature encoder. This 
     * is the same as GetCountsPerRevolution
     * 
     * For a description on the difference between CPR, PPR, etc. go to
     * https://www.cuidevices.com/blog/what-is-encoder-ppr-cpr-and-lpr
     * 
     * @return Counts per revolution
     */
    [[deprecated("use GetCountsPerRevolution() instead")]]
    uint32_t GetCPR();

    /**
     * Get the counts per revolution of the quadrature encoder.
     * 
     * For a description on the difference between CPR, PPR, etc. go to
     * https://www.cuidevices.com/blog/what-is-encoder-ppr-cpr-and-lpr
     * 
     * @return Counts per revolution
     */
    uint32_t GetCountsPerRevolution();

    /**
     * Set the phase of the CANSensor so that it is set to be in 
     * phase with the motor itself. This only works for quadrature
     * encoders. This will throw an error if the user tries to set
     * inverted while the SparkMax is Brushless and using the hall 
     * effect sensor.
     * 
     * @param inverted The phase of the encoder
     * 
     * @return CANError.kOK if successful
     */
    CANError SetInverted(bool inverted) override;

    /**
     * Get the phase of the CANSensor. This will just return false
     * if the user tries to get inverted while the SparkMax is 
     * Brushless and using the hall effect sensor.
     * 
     * @return The phase of the encoder
     */
    bool GetInverted() const override;

private:
    int m_counts_per_rev = 4096;

    std::atomic<bool> m_encInitialized = ATOMIC_VAR_INIT(false);
    std::atomic<bool> m_altEncInitialized = ATOMIC_VAR_INIT(false);


protected:
    int GetID() const override;
};

}  // namespace rev
