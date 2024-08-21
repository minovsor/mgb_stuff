function [lat, lon] = utm2deg(Easting, Northing, ZoneNumber, Hemisphere)
    % utm2deg converts UTM coordinates to latitude and longitude
    % Easting: UTM Easting coordinate
    % Northing: UTM Northing coordinate
    % ZoneNumber: UTM zone number
    % Hemisphere: 'N' for Northern Hemisphere, 'S' for Southern Hemisphere

    % Constants
    a = 6378137.0; % WGS84 major axis
    e = 0.0818191908; % WGS84 first eccentricity squared
    k0 = 0.9996; % Scale factor

    % Calculate the meridian
    lon_origin = (ZoneNumber - 1) * 6 - 180 + 3;

    % Calculate the footpoint latitude
    M = Northing / k0;
    mu = M / (a * (1 - e^2 / 4 - 3 * e^4 / 64 - 5 * e^6 / 256));

    % Calculate the latitude
    e1 = (1 - sqrt(1 - e^2)) / (1 + sqrt(1 - e^2));
    J1 = (3 * e1 / 2 - 27 * e1^3 / 32);
    J2 = (21 * e1^2 / 16 - 55 * e1^4 / 32);
    J3 = (151 * e1^3 / 96);
    J4 = (1097 * e1^4 / 512);
    fp = mu + J1 * sin(2 * mu) + J2 * sin(4 * mu) + J3 * sin(6 * mu) + J4 * sin(8 * mu);

    % Calculate latitude and longitude
    e2 = (e^2) / (1 - e^2);
    C1 = e2 * cos(fp)^2;
    T1 = tan(fp)^2;
    R1 = a * (1 - e^2) / (1 - e^2 * sin(fp)^2)^1.5;
    N1 = a / sqrt(1 - e^2 * sin(fp)^2);
    D = (Easting - 500000) / (N1 * k0);

    Q1 = N1 * tan(fp) / R1;
    Q2 = (D^2 / 2);
    Q3 = (5 + 3 * T1 + 10 * C1 - 4 * C1^2 - 9 * e2) * D^4 / 24;
    Q4 = (61 + 90 * T1 + 298 * C1 + 45 * T1^2 - 252 * e2 - 3 * C1^2) * D^6 / 720;

    lat = fp - Q1 * (Q2 - Q3 + Q4);

    Q5 = D;
    Q6 = (1 + 2 * T1 + C1) * D^3 / 6;
    Q7 = (5 - 2 * C1 + 28 * T1 - 3 * C1^2 + 8 * e2 + 24 * T1^2) * D^5 / 120;

    lon = lon_origin + (Q5 - Q6 + Q7) / cos(fp);

    % Convert radians to degrees
    lat = lat * 180 / pi;
    lon = lon * 180 / pi;

    % Adjust latitude for the Southern Hemisphere
    if strcmp(Hemisphere, 'S')
        lat = -lat;
    end
end