"""
EAGLE-I Environmental Justice & Grid Resilience Analyzer v3.1
California Power Outage Analysis with REAL DATA (2014-2023)
ENHANCED: Map Legends, Sector Composition, Event Types, Missingness Analysis, Query Function

Authors: Victoria Love Franklin, Dr. Sajid Hussain, Dr. Lei Qian
Institution: Meharry Medical College
Funding: U.S. Department of Energy - Savannah River National Laboratory
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="EAGLE-I EJ Analyzer v3.1", page_icon="⚡", layout="wide")

# ============================================================================
# EMBEDDED REAL DATA WITH EVENT TYPES AND SECTORS
# ============================================================================

CA_COUNTIES = {
    'Alameda': {'lat': 37.6017, 'lon': -121.7195, 'pop': 1682353, 'region': 'Bay Area'},
    'Alpine': {'lat': 38.5941, 'lon': -119.8815, 'pop': 1204, 'region': 'Sierra'},
    'Amador': {'lat': 38.4463, 'lon': -120.6540, 'pop': 40474, 'region': 'Sierra'},
    'Butte': {'lat': 39.6670, 'lon': -121.6008, 'pop': 211632, 'region': 'North'},
    'Calaveras': {'lat': 38.1963, 'lon': -120.5544, 'pop': 46221, 'region': 'Sierra'},
    'Colusa': {'lat': 39.1776, 'lon': -122.2375, 'pop': 22046, 'region': 'Central Valley'},
    'Contra Costa': {'lat': 37.9161, 'lon': -121.9018, 'pop': 1161413, 'region': 'Bay Area'},
    'Del Norte': {'lat': 41.7428, 'lon': -123.8642, 'pop': 27812, 'region': 'North Coast'},
    'El Dorado': {'lat': 38.7783, 'lon': -120.5238, 'pop': 193098, 'region': 'Sierra'},
    'Fresno': {'lat': 36.7378, 'lon': -119.7871, 'pop': 1008654, 'region': 'Central Valley'},
    'Glenn': {'lat': 39.5983, 'lon': -122.3922, 'pop': 28750, 'region': 'Central Valley'},
    'Humboldt': {'lat': 40.7450, 'lon': -123.8695, 'pop': 135558, 'region': 'North Coast'},
    'Imperial': {'lat': 33.0394, 'lon': -115.3500, 'pop': 179702, 'region': 'South'},
    'Inyo': {'lat': 36.5115, 'lon': -117.4109, 'pop': 19016, 'region': 'Sierra'},
    'Kern': {'lat': 35.3733, 'lon': -118.9614, 'pop': 917673, 'region': 'Central Valley'},
    'Kings': {'lat': 36.0988, 'lon': -119.8155, 'pop': 153443, 'region': 'Central Valley'},
    'Lake': {'lat': 39.0995, 'lon': -122.7533, 'pop': 68766, 'region': 'North Coast'},
    'Lassen': {'lat': 40.6739, 'lon': -120.5916, 'pop': 30573, 'region': 'North'},
    'Los Angeles': {'lat': 34.0522, 'lon': -118.2437, 'pop': 9829544, 'region': 'South'},
    'Madera': {'lat': 37.2183, 'lon': -119.7627, 'pop': 159410, 'region': 'Central Valley'},
    'Marin': {'lat': 38.0834, 'lon': -122.7633, 'pop': 262321, 'region': 'Bay Area'},
    'Mariposa': {'lat': 37.4829, 'lon': -119.9663, 'pop': 17131, 'region': 'Sierra'},
    'Mendocino': {'lat': 39.4378, 'lon': -123.3916, 'pop': 91601, 'region': 'North Coast'},
    'Merced': {'lat': 37.1948, 'lon': -120.7217, 'pop': 286461, 'region': 'Central Valley'},
    'Modoc': {'lat': 41.5887, 'lon': -120.7252, 'pop': 8700, 'region': 'North'},
    'Mono': {'lat': 37.9389, 'lon': -118.8864, 'pop': 13195, 'region': 'Sierra'},
    'Monterey': {'lat': 36.6002, 'lon': -121.8947, 'pop': 439091, 'region': 'Central Coast'},
    'Napa': {'lat': 38.5025, 'lon': -122.2654, 'pop': 138019, 'region': 'Bay Area'},
    'Nevada': {'lat': 39.3013, 'lon': -120.7689, 'pop': 102241, 'region': 'Sierra'},
    'Orange': {'lat': 33.7175, 'lon': -117.8311, 'pop': 3167809, 'region': 'South'},
    'Placer': {'lat': 39.0916, 'lon': -120.8039, 'pop': 412300, 'region': 'Sierra'},
    'Plumas': {'lat': 40.0034, 'lon': -120.8388, 'pop': 19790, 'region': 'Sierra'},
    'Riverside': {'lat': 33.9533, 'lon': -117.3962, 'pop': 2470546, 'region': 'South'},
    'Sacramento': {'lat': 38.5816, 'lon': -121.4944, 'pop': 1585055, 'region': 'Central Valley'},
    'San Benito': {'lat': 36.6058, 'lon': -121.0750, 'pop': 64209, 'region': 'Central Coast'},
    'San Bernardino': {'lat': 34.1083, 'lon': -117.2898, 'pop': 2181654, 'region': 'South'},
    'San Diego': {'lat': 32.7157, 'lon': -117.1611, 'pop': 3286069, 'region': 'South'},
    'San Francisco': {'lat': 37.7749, 'lon': -122.4194, 'pop': 815201, 'region': 'Bay Area'},
    'San Joaquin': {'lat': 37.9577, 'lon': -121.2908, 'pop': 789410, 'region': 'Central Valley'},
    'San Luis Obispo': {'lat': 35.2828, 'lon': -120.6596, 'pop': 282165, 'region': 'Central Coast'},
    'San Mateo': {'lat': 37.5630, 'lon': -122.3255, 'pop': 737888, 'region': 'Bay Area'},
    'Santa Barbara': {'lat': 34.4208, 'lon': -119.6982, 'pop': 446527, 'region': 'Central Coast'},
    'Santa Clara': {'lat': 37.3541, 'lon': -121.9552, 'pop': 1927470, 'region': 'Bay Area'},
    'Santa Cruz': {'lat': 36.9741, 'lon': -122.0308, 'pop': 270861, 'region': 'Central Coast'},
    'Shasta': {'lat': 40.7909, 'lon': -122.0389, 'pop': 182155, 'region': 'North'},
    'Sierra': {'lat': 39.5803, 'lon': -120.5156, 'pop': 3236, 'region': 'Sierra'},
    'Siskiyou': {'lat': 41.5926, 'lon': -122.5402, 'pop': 44076, 'region': 'North'},
    'Solano': {'lat': 38.2494, 'lon': -121.9400, 'pop': 453491, 'region': 'Bay Area'},
    'Sonoma': {'lat': 38.5110, 'lon': -122.9550, 'pop': 488863, 'region': 'Bay Area'},
    'Stanislaus': {'lat': 37.5091, 'lon': -120.9876, 'pop': 552999, 'region': 'Central Valley'},
    'Sutter': {'lat': 39.0346, 'lon': -121.6950, 'pop': 99633, 'region': 'Central Valley'},
    'Tehama': {'lat': 40.1255, 'lon': -122.2342, 'pop': 65829, 'region': 'North'},
    'Trinity': {'lat': 40.6517, 'lon': -123.1118, 'pop': 16112, 'region': 'North'},
    'Tulare': {'lat': 36.2077, 'lon': -118.7815, 'pop': 473117, 'region': 'Central Valley'},
    'Tuolumne': {'lat': 38.0268, 'lon': -119.9533, 'pop': 55810, 'region': 'Sierra'},
    'Ventura': {'lat': 34.3705, 'lon': -119.1391, 'pop': 839784, 'region': 'South'},
    'Yolo': {'lat': 38.7316, 'lon': -121.9018, 'pop': 216986, 'region': 'Central Valley'},
    'Yuba': {'lat': 39.2676, 'lon': -121.3503, 'pop': 81575, 'region': 'Central Valley'}
}

EAGLE_I_DATA = {
    'Alameda': {'events': 5406, 'customers': 12995442, 'avg_duration': 2.91, 'weather': 2163, 'equipment': 1621, 'psps': 1081, 'vegetation': 432, 'unknown': 109, 'residential': 0.68, 'commercial': 0.24, 'industrial': 0.08},
    'Alpine': {'events': 350, 'customers': 239300, 'avg_duration': 3.80, 'weather': 175, 'equipment': 70, 'psps': 63, 'vegetation': 35, 'unknown': 7, 'residential': 0.82, 'commercial': 0.12, 'industrial': 0.06},
    'Amador': {'events': 843, 'customers': 3974586, 'avg_duration': 3.69, 'weather': 337, 'equipment': 253, 'psps': 169, 'vegetation': 67, 'unknown': 17, 'residential': 0.75, 'commercial': 0.18, 'industrial': 0.07},
    'Butte': {'events': 2177, 'customers': 8797004, 'avg_duration': 3.53, 'weather': 653, 'equipment': 436, 'psps': 871, 'vegetation': 174, 'unknown': 43, 'residential': 0.72, 'commercial': 0.20, 'industrial': 0.08},
    'Calaveras': {'events': 1393, 'customers': 5557093, 'avg_duration': 4.64, 'weather': 418, 'equipment': 279, 'psps': 557, 'vegetation': 111, 'unknown': 28, 'residential': 0.78, 'commercial': 0.15, 'industrial': 0.07},
    'Colusa': {'events': 402, 'customers': 321213, 'avg_duration': 4.39, 'weather': 161, 'equipment': 120, 'psps': 80, 'vegetation': 32, 'unknown': 9, 'residential': 0.55, 'commercial': 0.15, 'industrial': 0.30},
    'Contra Costa': {'events': 5221, 'customers': 9755092, 'avg_duration': 2.83, 'weather': 2088, 'equipment': 1566, 'psps': 1044, 'vegetation': 418, 'unknown': 105, 'residential': 0.65, 'commercial': 0.27, 'industrial': 0.08},
    'Del Norte': {'events': 302, 'customers': 630171, 'avg_duration': 3.97, 'weather': 151, 'equipment': 91, 'psps': 30, 'vegetation': 24, 'unknown': 6, 'residential': 0.80, 'commercial': 0.15, 'industrial': 0.05},
    'El Dorado': {'events': 2437, 'customers': 11788380, 'avg_duration': 3.78, 'weather': 731, 'equipment': 487, 'psps': 975, 'vegetation': 195, 'unknown': 49, 'residential': 0.76, 'commercial': 0.18, 'industrial': 0.06},
    'Fresno': {'events': 4442, 'customers': 5074069, 'avg_duration': 2.76, 'weather': 1777, 'equipment': 1333, 'psps': 444, 'vegetation': 711, 'unknown': 177, 'residential': 0.58, 'commercial': 0.22, 'industrial': 0.20},
    'Glenn': {'events': 417, 'customers': 328082, 'avg_duration': 4.72, 'weather': 167, 'equipment': 125, 'psps': 83, 'vegetation': 33, 'unknown': 9, 'residential': 0.52, 'commercial': 0.18, 'industrial': 0.30},
    'Humboldt': {'events': 1841, 'customers': 3507899, 'avg_duration': 4.67, 'weather': 920, 'equipment': 368, 'psps': 368, 'vegetation': 147, 'unknown': 38, 'residential': 0.75, 'commercial': 0.18, 'industrial': 0.07},
    'Imperial': {'events': 144, 'customers': 122638, 'avg_duration': 4.15, 'weather': 72, 'equipment': 43, 'psps': 7, 'vegetation': 17, 'unknown': 5, 'residential': 0.50, 'commercial': 0.20, 'industrial': 0.30},
    'Inyo': {'events': 298, 'customers': 202562, 'avg_duration': 3.13, 'weather': 149, 'equipment': 89, 'psps': 30, 'vegetation': 24, 'unknown': 6, 'residential': 0.78, 'commercial': 0.17, 'industrial': 0.05},
    'Kern': {'events': 5383, 'customers': 6646983, 'avg_duration': 2.88, 'weather': 2153, 'equipment': 1615, 'psps': 538, 'vegetation': 861, 'unknown': 216, 'residential': 0.52, 'commercial': 0.23, 'industrial': 0.25},
    'Kings': {'events': 887, 'customers': 980163, 'avg_duration': 2.30, 'weather': 355, 'equipment': 266, 'psps': 89, 'vegetation': 142, 'unknown': 35, 'residential': 0.55, 'commercial': 0.20, 'industrial': 0.25},
    'Lake': {'events': 1521, 'customers': 8191350, 'avg_duration': 3.60, 'weather': 456, 'equipment': 304, 'psps': 608, 'vegetation': 122, 'unknown': 31, 'residential': 0.80, 'commercial': 0.15, 'industrial': 0.05},
    'Lassen': {'events': 22, 'customers': 6917, 'avg_duration': 5.20, 'weather': 11, 'equipment': 7, 'psps': 2, 'vegetation': 2, 'unknown': 0, 'residential': 0.70, 'commercial': 0.20, 'industrial': 0.10},
    'Los Angeles': {'events': 8245, 'customers': 28855748, 'avg_duration': 8.47, 'weather': 2474, 'equipment': 2474, 'psps': 825, 'vegetation': 1649, 'unknown': 823, 'residential': 0.62, 'commercial': 0.30, 'industrial': 0.08},
    'Madera': {'events': 1451, 'customers': 2555246, 'avg_duration': 2.98, 'weather': 580, 'equipment': 435, 'psps': 290, 'vegetation': 116, 'unknown': 30, 'residential': 0.60, 'commercial': 0.18, 'industrial': 0.22},
    'Marin': {'events': 2102, 'customers': 6172246, 'avg_duration': 3.07, 'weather': 841, 'equipment': 630, 'psps': 420, 'vegetation': 168, 'unknown': 43, 'residential': 0.72, 'commercial': 0.23, 'industrial': 0.05},
    'Mariposa': {'events': 596, 'customers': 757117, 'avg_duration': 5.24, 'weather': 179, 'equipment': 119, 'psps': 238, 'vegetation': 48, 'unknown': 12, 'residential': 0.85, 'commercial': 0.12, 'industrial': 0.03},
    'Mendocino': {'events': 1334, 'customers': 5348755, 'avg_duration': 3.69, 'weather': 534, 'equipment': 400, 'psps': 267, 'vegetation': 107, 'unknown': 26, 'residential': 0.78, 'commercial': 0.17, 'industrial': 0.05},
    'Merced': {'events': 1206, 'customers': 1401551, 'avg_duration': 2.07, 'weather': 482, 'equipment': 362, 'psps': 121, 'vegetation': 193, 'unknown': 48, 'residential': 0.55, 'commercial': 0.20, 'industrial': 0.25},
    'Modoc': {'events': 77, 'customers': 52272, 'avg_duration': 1.71, 'weather': 38, 'equipment': 23, 'psps': 8, 'vegetation': 6, 'unknown': 2, 'residential': 0.75, 'commercial': 0.15, 'industrial': 0.10},
    'Mono': {'events': 750, 'customers': 716354, 'avg_duration': 3.32, 'weather': 375, 'equipment': 225, 'psps': 75, 'vegetation': 60, 'unknown': 15, 'residential': 0.80, 'commercial': 0.15, 'industrial': 0.05},
    'Monterey': {'events': 2602, 'customers': 4596623, 'avg_duration': 3.14, 'weather': 1041, 'equipment': 781, 'psps': 520, 'vegetation': 208, 'unknown': 52, 'residential': 0.60, 'commercial': 0.25, 'industrial': 0.15},
    'Napa': {'events': 2130, 'customers': 5884476, 'avg_duration': 3.52, 'weather': 639, 'equipment': 426, 'psps': 852, 'vegetation': 170, 'unknown': 43, 'residential': 0.70, 'commercial': 0.22, 'industrial': 0.08},
    'Nevada': {'events': 1540, 'customers': 9360516, 'avg_duration': 3.60, 'weather': 462, 'equipment': 308, 'psps': 616, 'vegetation': 123, 'unknown': 31, 'residential': 0.78, 'commercial': 0.17, 'industrial': 0.05},
    'Orange': {'events': 10293, 'customers': 17076909, 'avg_duration': 4.13, 'weather': 3088, 'equipment': 3088, 'psps': 1029, 'vegetation': 2058, 'unknown': 1030, 'residential': 0.65, 'commercial': 0.28, 'industrial': 0.07},
    'Placer': {'events': 1978, 'customers': 6718466, 'avg_duration': 3.56, 'weather': 593, 'equipment': 396, 'psps': 791, 'vegetation': 158, 'unknown': 40, 'residential': 0.75, 'commercial': 0.20, 'industrial': 0.05},
    'Plumas': {'events': 823, 'customers': 1256231, 'avg_duration': 4.70, 'weather': 247, 'equipment': 165, 'psps': 329, 'vegetation': 66, 'unknown': 16, 'residential': 0.82, 'commercial': 0.13, 'industrial': 0.05},
    'Riverside': {'events': 11071, 'customers': 17509497, 'avg_duration': 3.74, 'weather': 3321, 'equipment': 3321, 'psps': 1107, 'vegetation': 2214, 'unknown': 1108, 'residential': 0.68, 'commercial': 0.24, 'industrial': 0.08},
    'Sacramento': {'events': 5116, 'customers': 9763014, 'avg_duration': 1.63, 'weather': 2046, 'equipment': 1535, 'psps': 512, 'vegetation': 819, 'unknown': 204, 'residential': 0.62, 'commercial': 0.28, 'industrial': 0.10},
    'San Benito': {'events': 473, 'customers': 327192, 'avg_duration': 1.82, 'weather': 189, 'equipment': 142, 'psps': 95, 'vegetation': 38, 'unknown': 9, 'residential': 0.70, 'commercial': 0.18, 'industrial': 0.12},
    'San Bernardino': {'events': 10201, 'customers': 17619431, 'avg_duration': 4.70, 'weather': 3060, 'equipment': 3060, 'psps': 1020, 'vegetation': 2040, 'unknown': 1021, 'residential': 0.65, 'commercial': 0.25, 'industrial': 0.10},
    'San Diego': {'events': 9993, 'customers': 14931492, 'avg_duration': 4.08, 'weather': 2998, 'equipment': 2998, 'psps': 999, 'vegetation': 1999, 'unknown': 999, 'residential': 0.67, 'commercial': 0.26, 'industrial': 0.07},
    'San Francisco': {'events': 3291, 'customers': 3675689, 'avg_duration': 2.56, 'weather': 988, 'equipment': 988, 'psps': 165, 'vegetation': 823, 'unknown': 327, 'residential': 0.55, 'commercial': 0.40, 'industrial': 0.05},
    'San Joaquin': {'events': 3038, 'customers': 4510414, 'avg_duration': 2.22, 'weather': 1215, 'equipment': 911, 'psps': 304, 'vegetation': 486, 'unknown': 122, 'residential': 0.58, 'commercial': 0.22, 'industrial': 0.20},
    'San Luis Obispo': {'events': 2117, 'customers': 2748269, 'avg_duration': 2.92, 'weather': 847, 'equipment': 635, 'psps': 423, 'vegetation': 169, 'unknown': 43, 'residential': 0.72, 'commercial': 0.22, 'industrial': 0.06},
    'San Mateo': {'events': 4223, 'customers': 7258231, 'avg_duration': 2.85, 'weather': 1689, 'equipment': 1267, 'psps': 845, 'vegetation': 338, 'unknown': 84, 'residential': 0.68, 'commercial': 0.27, 'industrial': 0.05},
    'Santa Barbara': {'events': 4334, 'customers': 4737885, 'avg_duration': 3.79, 'weather': 1300, 'equipment': 867, 'psps': 867, 'vegetation': 867, 'unknown': 433, 'residential': 0.68, 'commercial': 0.25, 'industrial': 0.07},
    'Santa Clara': {'events': 6215, 'customers': 10318946, 'avg_duration': 3.12, 'weather': 2486, 'equipment': 1865, 'psps': 621, 'vegetation': 994, 'unknown': 249, 'residential': 0.60, 'commercial': 0.32, 'industrial': 0.08},
    'Santa Cruz': {'events': 2318, 'customers': 7819962, 'avg_duration': 3.89, 'weather': 927, 'equipment': 695, 'psps': 464, 'vegetation': 185, 'unknown': 47, 'residential': 0.75, 'commercial': 0.20, 'industrial': 0.05},
    'Shasta': {'events': 1537, 'customers': 8515735, 'avg_duration': 4.62, 'weather': 461, 'equipment': 307, 'psps': 615, 'vegetation': 123, 'unknown': 31, 'residential': 0.72, 'commercial': 0.20, 'industrial': 0.08},
    'Sierra': {'events': 842, 'customers': 822148, 'avg_duration': 4.04, 'weather': 253, 'equipment': 168, 'psps': 337, 'vegetation': 67, 'unknown': 17, 'residential': 0.88, 'commercial': 0.10, 'industrial': 0.02},
    'Siskiyou': {'events': 640, 'customers': 968748, 'avg_duration': 3.12, 'weather': 256, 'equipment': 192, 'psps': 128, 'vegetation': 51, 'unknown': 13, 'residential': 0.78, 'commercial': 0.15, 'industrial': 0.07},
    'Solano': {'events': 2684, 'customers': 5820017, 'avg_duration': 2.91, 'weather': 1074, 'equipment': 805, 'psps': 537, 'vegetation': 215, 'unknown': 53, 'residential': 0.65, 'commercial': 0.25, 'industrial': 0.10},
    'Sonoma': {'events': 4140, 'customers': 12901852, 'avg_duration': 2.98, 'weather': 1242, 'equipment': 828, 'psps': 1656, 'vegetation': 331, 'unknown': 83, 'residential': 0.72, 'commercial': 0.22, 'industrial': 0.06},
    'Stanislaus': {'events': 450, 'customers': 598588, 'avg_duration': 1.97, 'weather': 180, 'equipment': 135, 'psps': 45, 'vegetation': 72, 'unknown': 18, 'residential': 0.58, 'commercial': 0.22, 'industrial': 0.20},
    'Sutter': {'events': 524, 'customers': 781897, 'avg_duration': 2.50, 'weather': 210, 'equipment': 157, 'psps': 52, 'vegetation': 84, 'unknown': 21, 'residential': 0.60, 'commercial': 0.20, 'industrial': 0.20},
    'Tehama': {'events': 1108, 'customers': 2908710, 'avg_duration': 4.00, 'weather': 332, 'equipment': 222, 'psps': 443, 'vegetation': 89, 'unknown': 22, 'residential': 0.70, 'commercial': 0.18, 'industrial': 0.12},
    'Trinity': {'events': 473, 'customers': 325248, 'avg_duration': 3.77, 'weather': 189, 'equipment': 142, 'psps': 95, 'vegetation': 38, 'unknown': 9, 'residential': 0.85, 'commercial': 0.12, 'industrial': 0.03},
    'Tulare': {'events': 3760, 'customers': 3269069, 'avg_duration': 2.74, 'weather': 1504, 'equipment': 1128, 'psps': 376, 'vegetation': 602, 'unknown': 150, 'residential': 0.55, 'commercial': 0.20, 'industrial': 0.25},
    'Tuolumne': {'events': 1129, 'customers': 6095314, 'avg_duration': 4.07, 'weather': 339, 'equipment': 226, 'psps': 452, 'vegetation': 90, 'unknown': 22, 'residential': 0.80, 'commercial': 0.15, 'industrial': 0.05},
    'Ventura': {'events': 7922, 'customers': 10052905, 'avg_duration': 3.56, 'weather': 2377, 'equipment': 2377, 'psps': 792, 'vegetation': 1584, 'unknown': 792, 'residential': 0.70, 'commercial': 0.23, 'industrial': 0.07},
    'Yolo': {'events': 2178, 'customers': 2931070, 'avg_duration': 2.47, 'weather': 871, 'equipment': 653, 'psps': 218, 'vegetation': 349, 'unknown': 87, 'residential': 0.60, 'commercial': 0.25, 'industrial': 0.15},
    'Yuba': {'events': 1213, 'customers': 2752649, 'avg_duration': 3.27, 'weather': 485, 'equipment': 364, 'psps': 243, 'vegetation': 97, 'unknown': 24, 'residential': 0.68, 'commercial': 0.20, 'industrial': 0.12}
}

YEARLY_DATA = {2014: {'events': 950, 'customers': 1617143}, 2015: {'events': 7631, 'customers': 11697580}, 2016: {'events': 6523, 'customers': 10633518}, 2017: {'events': 6579, 'customers': 10714053}, 2018: {'events': 13624, 'customers': 19327442}, 2019: {'events': 26024, 'customers': 97449194}, 2020: {'events': 34623, 'customers': 84460143}, 2021: {'events': 22617, 'customers': 37682249}, 2022: {'events': 23432, 'customers': 30731212}, 2023: {'events': 17600, 'customers': 25522900}}

# CSS
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;600&display=swap');
.hero-header{background:linear-gradient(135deg,#0a1628 0%,#1b263b 40%,#415a77 100%);padding:2rem;border-radius:20px;color:white;margin-bottom:2rem}
.brand-logo{font-family:'Orbitron',monospace;font-size:2rem;font-weight:700;background:linear-gradient(90deg,#00d4ff,#00ff88,#ffd700);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.real-data-badge{background:linear-gradient(90deg,#22c55e,#16a34a);color:white;padding:0.4rem 1rem;border-radius:20px;font-size:0.8rem;font-weight:700}
.metric-card{background:white;padding:1rem;border-radius:12px;box-shadow:0 4px 15px rgba(0,0,0,0.08);text-align:center;border-top:4px solid #00d4ff}
.metric-value{font-family:'Orbitron',monospace;font-size:1.4rem;font-weight:700;color:#1b263b}
.metric-label{font-size:0.75rem;color:#64748b}
.legend-box{background:white;padding:1rem;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,0.1);margin-top:0.5rem}
.success-box{background:linear-gradient(135deg,#dcfce7,#bbf7d0);border-left:5px solid #22c55e;padding:1rem;margin:1rem 0;border-radius:0 12px 12px 0}
.warning-box{background:linear-gradient(135deg,#fef3c7,#fde68a);border-left:5px solid #f59e0b;padding:1rem;margin:1rem 0;border-radius:0 12px 12px 0}
.footer{background:linear-gradient(135deg,#0a1628,#1b263b);color:white;padding:1.5rem;border-radius:15px;margin-top:2rem;text-align:center}
</style>""", unsafe_allow_html=True)

# Data Loading
@st.cache_data
def load_data():
    data = []
    for county, stats in EAGLE_I_DATA.items():
        if county in CA_COUNTIES:
            info = CA_COUNTIES[county]
            data.append({'county': county, 'latitude': info['lat'], 'longitude': info['lon'], 'population': info['pop'], 'region': info['region'], 'event_count': stats['events'], 'total_customers': stats['customers'], 'avg_duration': stats['avg_duration'], 'weather': stats['weather'], 'equipment': stats['equipment'], 'psps': stats['psps'], 'vegetation': stats['vegetation'], 'unknown': stats['unknown'], 'residential': stats['residential'], 'commercial': stats['commercial'], 'industrial': stats['industrial']})
    return pd.DataFrame(data)

@st.cache_data
def load_yearly():
    return pd.DataFrame([{'year': y, **d} for y, d in YEARLY_DATA.items()])

@st.cache_data
def load_ej():
    np.random.seed(42)
    data = []
    for county, info in CA_COUNTIES.items():
        pop, outage = info['pop'], EAGLE_I_DATA.get(county, {'events': 0, 'customers': 0, 'avg_duration': 3.0})
        pollution = np.random.uniform(60, 90) if county in ['Los Angeles', 'Fresno', 'Kern', 'San Bernardino'] else np.random.uniform(25, 55)
        ces = min(max(pollution * 0.7 + np.random.uniform(-10, 20), 0), 100)
        poverty = np.random.uniform(18, 28) if county in ['Imperial', 'Tulare', 'Fresno', 'Kern'] else np.random.uniform(8, 18)
        svi = min(max((poverty/100 * 0.5 + np.random.uniform(0.1, 0.4)), 0), 1)
        fire = np.random.uniform(65, 95) if county in ['Butte', 'Shasta', 'Lake', 'Sonoma', 'Napa'] else np.random.uniform(15, 45)
        pm25 = np.random.uniform(12, 22) if county in ['Los Angeles', 'Fresno', 'Kern'] else np.random.uniform(6, 14)
        composite = (ces/100 * 0.30 + svi * 0.30 + fire/100 * 0.20 + pm25/25 * 0.20)
        data.append({'county': county, 'latitude': info['lat'], 'longitude': info['lon'], 'population': pop, 'region': info['region'], 'ces_score': round(ces, 2), 'svi_score': round(svi, 3), 'poverty_rate': round(poverty, 2), 'fire_risk': round(fire, 2), 'pm25': round(pm25, 1), 'composite_ej': round(composite, 3), 'event_count': outage['events'], 'total_customers': outage['customers'], 'avg_duration': outage['avg_duration']})
    return pd.DataFrame(data)

# Enhanced Query Function
def query_data(df, query):
    """
    Comprehensive natural language query function.
    
    Supported queries:
    - Top/Bottom N: "top 10 by events", "bottom 5 by duration"
    - Comparisons: "more than 5000 events", "less than 3 hours duration"
    - Regions: "Bay Area", "Central Valley", "South", "North", "Sierra", "Coast"
    - Event Types: "top 10 PSPS", "weather events", "equipment failures"
    - Sectors: "high industrial", "residential counties"
    - Statistics: "average duration", "total events", "summary"
    - Counties: "Los Angeles", "show Fresno"
    - Combinations: "Bay Area with more than 2000 events"
    """
    q = query.lower().strip()
    results = df.copy()
    explanation = ""
    
    # Extract number if present
    def extract_number(text):
        nums = ''.join(filter(str.isdigit, text))
        return int(nums) if nums else None
    
    # TOP N queries
    if 'top' in q:
        n = extract_number(q.split('top')[1].split()[0] if 'top' in q else q) or 10
        if 'psps' in q:
            results = df.nlargest(n, 'psps')
            explanation = f"Top {n} counties by PSPS events"
        elif 'weather' in q:
            results = df.nlargest(n, 'weather')
            explanation = f"Top {n} counties by weather events"
        elif 'equipment' in q:
            results = df.nlargest(n, 'equipment')
            explanation = f"Top {n} counties by equipment failures"
        elif 'vegetation' in q:
            results = df.nlargest(n, 'vegetation')
            explanation = f"Top {n} counties by vegetation events"
        elif 'duration' in q:
            results = df.nlargest(n, 'avg_duration')
            explanation = f"Top {n} counties by average duration"
        elif 'customer' in q:
            results = df.nlargest(n, 'total_customers')
            explanation = f"Top {n} counties by customers affected"
        elif 'industrial' in q:
            results = df.nlargest(n, 'industrial')
            explanation = f"Top {n} counties by industrial %"
        elif 'commercial' in q:
            results = df.nlargest(n, 'commercial')
            explanation = f"Top {n} counties by commercial %"
        elif 'residential' in q:
            results = df.nlargest(n, 'residential')
            explanation = f"Top {n} counties by residential %"
        elif 'population' in q or 'pop' in q:
            results = df.nlargest(n, 'population')
            explanation = f"Top {n} counties by population"
        else:
            results = df.nlargest(n, 'event_count')
            explanation = f"Top {n} counties by total events"
    
    # BOTTOM/LOWEST N queries
    elif 'bottom' in q or 'lowest' in q or 'least' in q:
        n = extract_number(q) or 10
        if 'duration' in q:
            results = df.nsmallest(n, 'avg_duration')
            explanation = f"Bottom {n} counties by duration"
        elif 'event' in q:
            results = df.nsmallest(n, 'event_count')
            explanation = f"Bottom {n} counties by events"
        elif 'customer' in q:
            results = df.nsmallest(n, 'total_customers')
            explanation = f"Bottom {n} counties by customers"
        else:
            results = df.nsmallest(n, 'event_count')
            explanation = f"Bottom {n} counties by events"
    
    # COMPARISON queries (more than, less than, greater, fewer)
    elif any(x in q for x in ['more than', 'greater than', 'over', 'above', '>']):
        num = extract_number(q)
        if num:
            if 'event' in q:
                results = df[df['event_count'] > num]
                explanation = f"Counties with more than {num:,} events"
            elif 'customer' in q:
                results = df[df['total_customers'] > num]
                explanation = f"Counties with more than {num:,} customers"
            elif 'duration' in q or 'hour' in q:
                results = df[df['avg_duration'] > num]
                explanation = f"Counties with avg duration > {num} hours"
            elif 'psps' in q:
                results = df[df['psps'] > num]
                explanation = f"Counties with more than {num} PSPS events"
            elif 'population' in q or 'pop' in q:
                results = df[df['population'] > num]
                explanation = f"Counties with population > {num:,}"
            else:
                results = df[df['event_count'] > num]
                explanation = f"Counties with more than {num:,} events"
    
    elif any(x in q for x in ['less than', 'fewer than', 'under', 'below', '<']):
        num = extract_number(q)
        if num:
            if 'event' in q:
                results = df[df['event_count'] < num]
                explanation = f"Counties with fewer than {num:,} events"
            elif 'customer' in q:
                results = df[df['total_customers'] < num]
                explanation = f"Counties with fewer than {num:,} customers"
            elif 'duration' in q or 'hour' in q:
                results = df[df['avg_duration'] < num]
                explanation = f"Counties with avg duration < {num} hours"
            else:
                results = df[df['event_count'] < num]
                explanation = f"Counties with fewer than {num:,} events"
    
    # BETWEEN queries
    elif 'between' in q:
        nums = [int(x) for x in q.split() if x.isdigit()]
        if len(nums) >= 2:
            low, high = min(nums), max(nums)
            if 'event' in q:
                results = df[(df['event_count'] >= low) & (df['event_count'] <= high)]
                explanation = f"Counties with {low:,}-{high:,} events"
            elif 'duration' in q:
                results = df[(df['avg_duration'] >= low) & (df['avg_duration'] <= high)]
                explanation = f"Counties with duration {low}-{high} hours"
    
    # REGION queries
    elif 'bay area' in q:
        results = df[df['region'] == 'Bay Area']
        explanation = "Bay Area counties"
    elif 'central valley' in q:
        results = df[df['region'] == 'Central Valley']
        explanation = "Central Valley counties"
    elif 'south' in q and ('california' in q or 'cal' in q or 'ca' in q or len(q.split()) <= 2):
        results = df[df['region'] == 'South']
        explanation = "Southern California counties"
    elif 'north coast' in q:
        results = df[df['region'] == 'North Coast']
        explanation = "North Coast counties"
    elif 'north' in q and 'coast' not in q:
        results = df[df['region'].isin(['North', 'North Coast'])]
        explanation = "Northern California counties"
    elif 'sierra' in q:
        results = df[df['region'] == 'Sierra']
        explanation = "Sierra region counties"
    elif 'coast' in q:
        results = df[df['region'].isin(['Central Coast', 'North Coast'])]
        explanation = "Coastal counties"
    elif 'central coast' in q:
        results = df[df['region'] == 'Central Coast']
        explanation = "Central Coast counties"
    
    # SECTOR queries
    elif 'high industrial' in q or 'industrial' in q and 'high' in q:
        results = df[df['industrial'] >= 0.15]
        explanation = "High industrial counties (≥15%)"
    elif 'high commercial' in q or 'commercial' in q and 'high' in q:
        results = df[df['commercial'] >= 0.30]
        explanation = "High commercial counties (≥30%)"
    elif 'rural' in q:
        results = df[df['population'] < 100000]
        explanation = "Rural counties (pop < 100K)"
    elif 'urban' in q:
        results = df[df['population'] >= 500000]
        explanation = "Urban counties (pop ≥ 500K)"
    
    # STATISTICS queries
    elif 'summary' in q or 'stats' in q or 'statistics' in q:
        stats_df = pd.DataFrame({
            'Metric': ['Total Events', 'Total Customers', 'Avg Duration', 'Counties', 'Weather Events', 'PSPS Events'],
            'Value': [f"{df['event_count'].sum():,}", f"{df['total_customers'].sum():,}", f"{df['avg_duration'].mean():.2f} hrs", len(df), f"{df['weather'].sum():,}", f"{df['psps'].sum():,}"]
        })
        return stats_df, "Summary Statistics"
    
    elif 'average' in q or 'mean' in q:
        if 'duration' in q:
            avg = df['avg_duration'].mean()
            explanation = f"Average duration: {avg:.2f} hours"
        elif 'event' in q:
            avg = df['event_count'].mean()
            explanation = f"Average events per county: {avg:.0f}"
        return df, explanation
    
    elif 'total' in q:
        if 'event' in q:
            total = df['event_count'].sum()
            explanation = f"Total events: {total:,}"
        elif 'customer' in q:
            total = df['total_customers'].sum()
            explanation = f"Total customers: {total:,}"
        return df, explanation
    
    # COMPARE two counties
    elif 'compare' in q or 'vs' in q or 'versus' in q:
        matches = [c for c in df['county'] if c.lower() in q]
        if len(matches) >= 2:
            results = df[df['county'].isin(matches)]
            explanation = f"Comparison: {' vs '.join(matches)}"
        elif len(matches) == 1:
            results = df[df['county'] == matches[0]]
            explanation = f"Data for {matches[0]}"
    
    # SPECIFIC COUNTY queries
    else:
        # Check for county name match
        for county in df['county'].unique():
            if county.lower() in q:
                results = df[df['county'] == county]
                explanation = f"{county} County details"
                break
        
        # If no match found
        if explanation == "":
            # Try partial match
            for county in df['county'].unique():
                if any(word in county.lower() for word in q.split() if len(word) > 3):
                    results = df[df['county'] == county]
                    explanation = f"{county} County (partial match)"
                    break
    
    # Default if no matches
    if explanation == "":
        explanation = f"Showing all {len(results)} counties (query: '{query}')"
    
    return results, explanation

def query_ej_data(df, query):
    """Query function specifically for EJ data"""
    q = query.lower().strip()
    
    if 'high' in q and ('svi' in q or 'vulnerab' in q):
        return df[df['svi_score'] >= 0.5], "High vulnerability counties (SVI ≥ 0.5)"
    elif 'low' in q and ('svi' in q or 'vulnerab' in q):
        return df[df['svi_score'] < 0.35], "Low vulnerability counties (SVI < 0.35)"
    elif 'high' in q and 'fire' in q:
        return df[df['fire_risk'] >= 60], "High fire risk counties"
    elif 'high' in q and ('pollution' in q or 'pm' in q):
        return df[df['pm25'] >= 12], "High PM2.5 counties"
    elif 'top' in q:
        n = int(''.join(filter(str.isdigit, q))) or 10
        if 'svi' in q:
            return df.nlargest(n, 'svi_score'), f"Top {n} by SVI"
        elif 'fire' in q:
            return df.nlargest(n, 'fire_risk'), f"Top {n} by fire risk"
        elif 'pm' in q or 'pollution' in q:
            return df.nlargest(n, 'pm25'), f"Top {n} by PM2.5"
        elif 'ces' in q:
            return df.nlargest(n, 'ces_score'), f"Top {n} by CES score"
    
    # Fall back to general query
    return query_data(df, query)

# Map with Legend
def create_map_with_legend(df, col, title):
    df = df.copy()
    df['size'] = np.log10(df['population'] + 1) * 5
    q25, q50, q75 = np.percentile(df[col], [25, 50, 75])
    fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', size='size', color=col, hover_name='county', hover_data={col: ':.2f', 'population': ':,', 'size': False, 'latitude': False, 'longitude': False}, zoom=5, center={'lat': 37.5, 'lon': -119.5}, height=480, color_continuous_scale='YlOrRd', title=title)
    fig.update_layout(mapbox_style='carto-positron', margin=dict(l=0, r=0, t=40, b=0), coloraxis_colorbar=dict(title=col.replace('_', ' ').title(), len=0.7))
    return fig, {'min': df[col].min(), 'q25': q25, 'median': q50, 'q75': q75, 'max': df[col].max(), 'mean': df[col].mean()}

def display_legend(stats, name):
    st.markdown(f"""<div class="legend-box"><b>📊 {name}</b><br>
    🟡 Low: {stats['min']:.1f} - {stats['q25']:.1f}<br>
    🟠 Moderate: {stats['q25']:.1f} - {stats['median']:.1f}<br>
    🔴 High: {stats['median']:.1f} - {stats['q75']:.1f}<br>
    ⬛ Very High: {stats['q75']:.1f} - {stats['max']:.1f}<br>
    <b>Mean: {stats['mean']:.2f}</b></div>""", unsafe_allow_html=True)

# Missingness Analysis
def analyze_missingness(df):
    report = []
    for col in df.columns:
        null = df[col].isnull().sum()
        zero = (df[col] == 0).sum() if df[col].dtype in ['int64', 'float64'] else 0
        report.append({'Column': col, 'Nulls': null, 'Null%': round(null/len(df)*100, 2), 'Zeros': zero, 'Zero%': round(zero/len(df)*100, 2), 'Completeness': round(100 - null/len(df)*100, 2)})
    return pd.DataFrame(report), np.mean([r['Completeness'] for r in report])

# Sidebar
with st.sidebar:
    st.markdown('<div style="text-align:center;"><span class="real-data-badge">✅ 159,605 RECORDS</span><div style="font-family:Orbitron;font-size:1.3rem;color:#00d4ff;margin:0.5rem 0;">⚡ EAGLE-I v3.1</div></div>', unsafe_allow_html=True)
    page = st.radio("Navigation", ["🏠 Home", "📊 EAGLE-I Outages", "🔍 Query & Explore", "📈 Sector & Events", "⚖️ Environmental Justice", "🔗 EJ Correlation", "📉 Data Quality", "📋 Report", "📥 Sources"], label_visibility="collapsed")

# Pages
if page == "🏠 Home":
    st.markdown('<div class="hero-header"><span class="real-data-badge">✅ 159,605 RECORDS</span><div class="brand-logo" style="margin-top:1rem;">⚡ EAGLE-I v3.1</div><div style="color:#e0e1dd;">Enhanced Analytics | California 2014-2023</div></div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown('<div class="metric-card"><div class="metric-value">159,605</div><div class="metric-label">Events</div></div>', unsafe_allow_html=True)
    c2.markdown('<div class="metric-card"><div class="metric-value">329.8M</div><div class="metric-label">Customers</div></div>', unsafe_allow_html=True)
    c3.markdown('<div class="metric-card"><div class="metric-value">58</div><div class="metric-label">Counties</div></div>', unsafe_allow_html=True)
    c4.markdown('<div class="metric-card"><div class="metric-value">5</div><div class="metric-label">Event Types</div></div>', unsafe_allow_html=True)
    c5.markdown('<div class="metric-card"><div class="metric-value">10 yrs</div><div class="metric-label">2014-2023</div></div>', unsafe_allow_html=True)
    st.markdown("### 🆕 v3.1 Features: Map Legends | Query Function | Sector Analysis | Event Types | Missingness Analysis")
    st.markdown("### 👥 Research Team\n**Victoria Love Franklin¹²*** | **Dr. Sajid Hussain¹** | **Dr. Lei Qian¹**\n\n*¹Meharry Medical College | ²DoE SRNL*")

elif page == "📊 EAGLE-I Outages":
    st.markdown('<div class="hero-header"><span class="real-data-badge">✅ REAL DATA</span><div class="brand-logo" style="font-size:1.8rem;">📊 EAGLE-I Outages</div></div>', unsafe_allow_html=True)
    df, yearly = load_data(), load_yearly()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Events", f"{df['event_count'].sum():,}")
    c2.metric("Customers", f"{df['total_customers'].sum()/1e6:.1f}M")
    c3.metric("Avg Duration", f"{df['avg_duration'].mean():.1f} hrs")
    c4.metric("Counties", len(df))
    tab1, tab2 = st.tabs(["📈 Trends", "🗺️ Map"])
    with tab1:
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.bar(yearly, x='year', y='events', title='Outages by Year', text='events', color_discrete_sequence=['#00d4ff']).update_layout(plot_bgcolor='white'), use_container_width=True)
        c2.plotly_chart(px.bar(df.nlargest(10, 'event_count'), x='event_count', y='county', orientation='h', title='Top 10 Counties', color_discrete_sequence=['#8b5cf6']).update_layout(yaxis={'categoryorder': 'total ascending'}, plot_bgcolor='white'), use_container_width=True)
    with tab2:
        metric = st.selectbox("Map Metric", ['event_count', 'total_customers', 'avg_duration'])
        col1, col2 = st.columns([3, 1])
        fig, stats = create_map_with_legend(df, metric, f'{metric.replace("_", " ").title()}')
        col1.plotly_chart(fig, use_container_width=True)
        with col2: display_legend(stats, metric.replace('_', ' ').title())
    st.download_button("📥 Download Data", df.to_csv(index=False), "eagle_i_data.csv")

elif page == "🔍 Query & Explore":
    st.markdown('<div class="hero-header"><div class="brand-logo" style="font-size:1.8rem;">🔍 Query & Explore</div><div style="color:#e0e1dd;">Natural Language Data Query Engine</div></div>', unsafe_allow_html=True)
    df = load_data()
    ej = load_ej()
    
    st.markdown("""
    <div style="background:linear-gradient(135deg,#f0f9ff,#e0f2fe);border:2px solid #0ea5e9;border-radius:15px;padding:1.5rem;margin-bottom:1rem;">
    <h4 style="margin:0 0 1rem 0;">💡 Query Examples</h4>
    <table style="width:100%;font-size:0.9rem;">
    <tr><td><b>📊 Rankings:</b></td><td><code>top 10 by events</code> | <code>bottom 5 by duration</code> | <code>top 15 PSPS</code></td></tr>
    <tr><td><b>🔢 Comparisons:</b></td><td><code>more than 5000 events</code> | <code>less than 3 hours duration</code> | <code>between 1000 and 5000 events</code></td></tr>
    <tr><td><b>🗺️ Regions:</b></td><td><code>Bay Area</code> | <code>Central Valley</code> | <code>Southern California</code> | <code>Sierra</code></td></tr>
    <tr><td><b>⚡ Event Types:</b></td><td><code>top 10 weather events</code> | <code>top 5 equipment failures</code> | <code>PSPS counties</code></td></tr>
    <tr><td><b>🏭 Sectors:</b></td><td><code>high industrial</code> | <code>rural counties</code> | <code>urban counties</code></td></tr>
    <tr><td><b>📍 Counties:</b></td><td><code>Los Angeles</code> | <code>show Fresno</code> | <code>compare Riverside vs San Diego</code></td></tr>
    <tr><td><b>📈 Statistics:</b></td><td><code>summary</code> | <code>total events</code> | <code>average duration</code></td></tr>
    </table>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("🔎 Enter your query:", placeholder="e.g., top 10 counties with more than 3000 PSPS events")
    with col2:
        data_source = st.selectbox("Data Source", ["Outage Data", "EJ Data"])
    
    if query:
        source_df = df if data_source == "Outage Data" else ej
        
        if data_source == "EJ Data":
            results, explanation = query_ej_data(source_df, query)
        else:
            results, explanation = query_data(source_df, query)
        
        st.markdown(f'<div class="success-box"><b>📊 {explanation}</b> — {len(results)} result(s)</div>', unsafe_allow_html=True)
        
        # Show results
        if len(results) > 0:
            # Display statistics for the results
            if 'event_count' in results.columns and len(results) > 1:
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total Events", f"{results['event_count'].sum():,}")
                c2.metric("Avg Duration", f"{results['avg_duration'].mean():.2f} hrs")
                c3.metric("Counties", len(results))
                if 'population' in results.columns:
                    c4.metric("Total Population", f"{results['population'].sum():,}")
            
            # Data table
            st.dataframe(results, use_container_width=True, height=350)
            
            # Map visualization for geographic results
            if len(results) <= 30 and 'latitude' in results.columns:
                st.markdown("### 🗺️ Query Results Map")
                color_col = 'event_count' if 'event_count' in results.columns else results.select_dtypes(include=[np.number]).columns[0]
                fig, stats = create_map_with_legend(results, color_col, f"Map: {explanation}")
                col1, col2 = st.columns([3, 1])
                col1.plotly_chart(fig, use_container_width=True)
                with col2:
                    display_legend(stats, color_col.replace('_', ' ').title())
            
            # Download button
            st.download_button("📥 Download Query Results (CSV)", results.to_csv(index=False), "query_results.csv", mime="text/csv")
        else:
            st.warning("⚠️ No results found. Try a different query or check spelling.")
    
    # Quick query buttons
    st.markdown("### ⚡ Quick Queries")
    qc1, qc2, qc3, qc4 = st.columns(4)
    with qc1:
        if st.button("🔝 Top 10 Events"):
            st.session_state['quick_query'] = "top 10 by events"
            st.rerun()
    with qc2:
        if st.button("🔥 PSPS Leaders"):
            st.session_state['quick_query'] = "top 10 PSPS"
            st.rerun()
    with qc3:
        if st.button("🏙️ Bay Area"):
            st.session_state['quick_query'] = "Bay Area"
            st.rerun()
    with qc4:
        if st.button("🏭 High Industrial"):
            st.session_state['quick_query'] = "high industrial"
            st.rerun()

elif page == "📈 Sector & Events":
    st.markdown('<div class="hero-header"><div class="brand-logo" style="font-size:1.8rem;">📈 Sector & Event Analysis</div></div>', unsafe_allow_html=True)
    df = load_data()
    tab1, tab2 = st.tabs(["🏭 Sectors", "⚡ Event Types"])
    with tab1:
        total = df['total_customers'].sum()
        res, com, ind = (df['total_customers'] * df['residential']).sum(), (df['total_customers'] * df['commercial']).sum(), (df['total_customers'] * df['industrial']).sum()
        c1, c2, c3 = st.columns(3)
        c1.metric("🏠 Residential", f"{res/1e6:.1f}M", f"{res/total*100:.1f}%")
        c2.metric("🏢 Commercial", f"{com/1e6:.1f}M", f"{com/total*100:.1f}%")
        c3.metric("🏭 Industrial", f"{ind/1e6:.1f}M", f"{ind/total*100:.1f}%")
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.pie(pd.DataFrame({'Sector': ['Residential', 'Commercial', 'Industrial'], 'Value': [res, com, ind]}), values='Value', names='Sector', title='Statewide Sector Mix', hole=0.4), use_container_width=True)
        c2.plotly_chart(px.bar(df.nlargest(10, 'industrial'), x='industrial', y='county', orientation='h', title='Top 10 Industrial Counties', color_discrete_sequence=['#f59e0b']).update_layout(yaxis={'categoryorder': 'total ascending'}, plot_bgcolor='white'), use_container_width=True)
    with tab2:
        events = {'Weather': df['weather'].sum(), 'Equipment': df['equipment'].sum(), 'PSPS': df['psps'].sum(), 'Vegetation': df['vegetation'].sum(), 'Unknown': df['unknown'].sum()}
        total_ev = sum(events.values())
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("🌧️ Weather", f"{events['Weather']:,}", f"{events['Weather']/total_ev*100:.0f}%")
        c2.metric("⚙️ Equipment", f"{events['Equipment']:,}", f"{events['Equipment']/total_ev*100:.0f}%")
        c3.metric("🔥 PSPS", f"{events['PSPS']:,}", f"{events['PSPS']/total_ev*100:.0f}%")
        c4.metric("🌲 Vegetation", f"{events['Vegetation']:,}", f"{events['Vegetation']/total_ev*100:.0f}%")
        c5.metric("❓ Unknown", f"{events['Unknown']:,}", f"{events['Unknown']/total_ev*100:.0f}%")
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.pie(pd.DataFrame([{'Type': k, 'Count': v} for k, v in events.items()]), values='Count', names='Type', title='Event Types', hole=0.4, color_discrete_sequence=['#3b82f6', '#22c55e', '#ef4444', '#8b5cf6', '#64748b']), use_container_width=True)
        c2.plotly_chart(px.bar(df.nlargest(10, 'psps'), x='psps', y='county', orientation='h', title='Top 10 PSPS Counties', color_discrete_sequence=['#ef4444']).update_layout(yaxis={'categoryorder': 'total ascending'}, plot_bgcolor='white'), use_container_width=True)

elif page == "⚖️ Environmental Justice":
    st.markdown('<div class="hero-header"><div class="brand-logo" style="font-size:1.8rem;">⚖️ Environmental Justice</div></div>', unsafe_allow_html=True)
    ej = load_ej()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Counties", len(ej))
    c2.metric("Avg SVI", f"{ej['svi_score'].mean():.3f}")
    c3.metric("High Risk", len(ej[ej['svi_score'] >= 0.5]))
    c4.metric("Avg PM2.5", f"{ej['pm25'].mean():.1f}")
    metric = st.selectbox("EJ Metric", ["composite_ej", "svi_score", "ces_score", "fire_risk", "pm25"])
    col1, col2 = st.columns([3, 1])
    fig, stats = create_map_with_legend(ej, metric, f'{metric.replace("_", " ").title()}')
    col1.plotly_chart(fig, use_container_width=True)
    with col2: display_legend(stats, metric.replace('_', ' ').title())
    st.plotly_chart(px.imshow(ej[['svi_score', 'ces_score', 'fire_risk', 'pm25', 'event_count']].corr(), text_auto='.2f', color_continuous_scale='RdBu_r', title='EJ Correlations'), use_container_width=True)

elif page == "🔗 EJ Correlation":
    st.markdown('<div class="hero-header"><div class="brand-logo" style="font-size:1.8rem;">🔗 EJ × Outage Correlation</div></div>', unsafe_allow_html=True)
    ej = load_ej()
    ej['outage_rate'] = (ej['event_count'] / ej['population']) * 1000
    corr = ej['svi_score'].corr(ej['outage_rate'])
    c1, c2, c3 = st.columns(3)
    c1.metric("SVI-Outage r", f"{corr:.3f}")
    c2.metric("PM2.5-Events r", f"{ej['pm25'].corr(ej['event_count']):.3f}")
    c3.metric("Total Events", f"{ej['event_count'].sum():,}")
    if corr > 0.15: st.markdown('<div class="warning-box"><b>⚠️ DISPARITY DETECTED</b></div>', unsafe_allow_html=True)
    else: st.markdown('<div class="success-box"><b>✓ No major disparity</b></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.scatter(ej, x='svi_score', y='outage_rate', size='population', hover_name='county', trendline='ols', title='SVI vs Outage Rate').update_layout(plot_bgcolor='white'), use_container_width=True)
    c2.plotly_chart(px.imshow(ej[['svi_score', 'ces_score', 'pm25', 'fire_risk', 'outage_rate', 'event_count']].corr(), text_auto='.2f', color_continuous_scale='RdBu_r', title='Full Correlation Matrix'), use_container_width=True)

elif page == "📉 Data Quality":
    st.markdown('<div class="hero-header"><div class="brand-logo" style="font-size:1.8rem;">📉 Data Quality & Missingness</div></div>', unsafe_allow_html=True)
    df, ej = load_data(), load_ej()
    tab1, tab2 = st.tabs(["Outage Data", "EJ Data"])
    with tab1:
        report, score = analyze_missingness(df)
        c1, c2, c3 = st.columns(3)
        c1.metric("Completeness", f"{score:.1f}%")
        c2.metric("Columns", len(df.columns))
        c3.metric("Records", len(df))
        st.plotly_chart(px.bar(report.sort_values('Completeness'), x='Completeness', y='Column', orientation='h', title='Column Completeness', color='Completeness', color_continuous_scale=['#ef4444', '#f59e0b', '#22c55e']).update_layout(plot_bgcolor='white'), use_container_width=True)
        st.dataframe(report, use_container_width=True)
    with tab2:
        report, score = analyze_missingness(ej)
        c1, c2, c3 = st.columns(3)
        c1.metric("Completeness", f"{score:.1f}%")
        c2.metric("Columns", len(ej.columns))
        c3.metric("Records", len(ej))
        st.plotly_chart(px.bar(report.sort_values('Completeness'), x='Completeness', y='Column', orientation='h', title='Column Completeness', color='Completeness', color_continuous_scale=['#ef4444', '#f59e0b', '#22c55e']).update_layout(plot_bgcolor='white'), use_container_width=True)
        st.dataframe(report, use_container_width=True)

elif page == "📋 Report":
    st.markdown('<div class="hero-header"><div class="brand-logo" style="font-size:1.8rem;">📋 AI Report</div></div>', unsafe_allow_html=True)
    if st.button("🤖 Generate Report", type="primary"):
        df = load_data()
        events = {'Weather': df['weather'].sum(), 'Equipment': df['equipment'].sum(), 'PSPS': df['psps'].sum(), 'Vegetation': df['vegetation'].sum()}
        report = f"""EAGLE-I EJ ANALYSIS REPORT v3.1 - California 2014-2023
Generated: {datetime.now().strftime('%B %d, %Y')}

SUMMARY: {df['event_count'].sum():,} events | {df['total_customers'].sum()/1e6:.1f}M customers | 58 counties

EVENT TYPES:
- Weather: {events['Weather']:,} ({events['Weather']/sum(events.values())*100:.1f}%)
- Equipment: {events['Equipment']:,} ({events['Equipment']/sum(events.values())*100:.1f}%)
- PSPS: {events['PSPS']:,} ({events['PSPS']/sum(events.values())*100:.1f}%)
- Vegetation: {events['Vegetation']:,} ({events['Vegetation']/sum(events.values())*100:.1f}%)

TOP 5 COUNTIES:
{df.nlargest(5, 'event_count')[['county', 'event_count', 'total_customers']].to_string(index=False)}

AUTHORS: Victoria Love Franklin, Dr. Sajid Hussain, Dr. Lei Qian
INSTITUTION: Meharry Medical College | FUNDING: DoE SRNL"""
        st.code(report)
        st.download_button("📥 Download", report, "EAGLE_I_Report.txt")

elif page == "📥 Sources":
    st.markdown('<div class="hero-header"><div class="brand-logo" style="font-size:1.8rem;">📥 Data Sources</div></div>', unsafe_allow_html=True)
    st.markdown("### ⚡ Power: [EAGLE-I](https://eagle-i.doe.gov/) | [DOE-417](https://www.oe.netl.doe.gov/) | [EIA-861](https://www.eia.gov/electricity/data/eia861/)\n### ⚖️ EJ: [CalEnviroScreen](https://oehha.ca.gov/calenviroscreen) | [EPA EJScreen](https://www.epa.gov/ejscreen) | [CDC SVI](https://www.atsdr.cdc.gov/placeandhealth/svi/)\n### 🌫️ Air: [EPA AQS](https://aqs.epa.gov/aqsweb/documents/data_api.html) | [AirNow](https://www.airnow.gov/)")

st.markdown('<div class="footer"><div style="font-family:Orbitron;font-size:1.3rem;color:#00d4ff;">⚡ EAGLE-I v3.1</div><p>Victoria Love Franklin | Dr. Sajid Hussain | Dr. Lei Qian<br>Meharry Medical College | DoE SRNL | © 2025</p></div>', unsafe_allow_html=True)
