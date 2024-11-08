// SUBROUTINE LOCAL VARIABLE DECLARATIONS:
int FacadeNum;         // Facade number
int ExtNum;            // External number
int AFNZnNum;          // Zone number
Real64 SideRatio;      // For vertical facades, width of facade / width of adjacent facade
Real64 SR;             // SideRatio restricted to 0.25 to 4.0 range
Real64 SideRatioFac;   // LOG(SideRatio)
Real64 IncRad;         // IncAng in radians
int IAng;              // Incidence angle index; used in interpolation
Real64 DelAng;         // Incidence angle difference; used in interpolation
Real64 WtAng;          // Incidence angle weighting factor; used in interpolation
int ISR;               // Side ratio index, for interpolation
Real64 WtSR;           // Side ratio weighting factor; used in interpolation
int SurfNum;           // Surface number
int SurfDatNum;        // Surface data number
Real64 SurfAng;        // Azimuth angle of surface normal (degrees clockwise from North)
int FacadeNumThisSurf; // Facade number for a particular surface
Real64 AngDiff;        // Angle difference between wind and surface direction (deg)
Real64 AngDiffMin;     // Minimum angle difference between wind and surface direction (deg)
std::vector<int> curveIndex = {0, 0, 0, 0, 0};



std::vector<Real64> vals(13);
for (int windDirNum = 1; windDirNum <= 12; ++windDirNum) {
    Real64 WindAng = (windDirNum - 1) * 30.0;
    IncAng = std::abs(WindAng - FacadeAng(FacadeNum));
    if (IncAng > 180.0) IncAng = 360.0 - IncAng;
    IAng = int(IncAng / 30.0) + 1;
    DelAng = mod(IncAng, 30.0);
    WtAng = 1.0 - DelAng / 30.0;

    // Wind-pressure coefficients for vertical facades, low-rise building

    if (Util::SameString(simulation_control.BldgType, "LowRise") && FacadeNum <= 4) {
        IncRad = IncAng * Constant::DegToRadians;
        Real64 const cos_IncRad_over_2(std::cos(IncRad / 2.0));
        vals[windDirNum - 1] = 0.6 * std::log(1.248 - 0.703 * std::sin(IncRad / 2.0) - 1.175 * pow_2(std::sin(IncRad)) +
        0.131 * pow_3(std::sin(2.0 * IncRad * SideRatioFac)) + 0.769 * cos_IncRad_over_2 +
        0.07 * pow_2(SideRatioFac * std::sin(IncRad / 2.0)) + 0.717 * pow_2(cos_IncRad_over_2));
    }