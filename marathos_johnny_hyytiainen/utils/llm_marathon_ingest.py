# LLM-generated synthetic marathon data ingestion
# Source: Gemini generated 50 rows of realistic ultramarathon data
# for "Stockholm Marathos Ultra (SWE)" 2023-03-15
# LLM used for data generation only, not for pipeline logic
import csv

CSV_DATA = """Year of event,Event dates,Event name,Event distance/length,Event number of finishers,Athlete performance,Athlete club,Athlete country,Athlete year of birth,Athlete gender,Athlete age category,Athlete average speed,Athlete ID
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,08:12:30 h,IF Linnéa,SWE,1985,M,M35,12.183,2000000
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,08:24:15 h,Oslo IL,NOR,1980,F,W40,11.899,2000001
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,08:35:50 h,Helsinki Runners,FIN,1976,M,M45,11.632,2000002
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,08:42:10 h,Copenhagen Athletics,DNK,1971,M,M50,11.491,2000003
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,08:55:05 h,IF Linnéa,SWE,1988,F,W35,11.213,2000004
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,09:03:20 h,Oslo IL,NOR,1975,F,W45,11.043,2000005
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,09:12:45 h,Helsinki Runners,FIN,1982,M,M40,10.855,2000006
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,09:18:30 h,IF Linnéa,SWE,1977,M,M45,10.743,2000007
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,09:25:15 h,Copenhagen Athletics,DNK,1987,M,M35,10.615,2000008
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,09:33:40 h,Oslo IL,NOR,1970,M,M50,10.459,2000009
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,09:41:55 h,IF Linnéa,SWE,1979,F,W40,10.311,2000010
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,09:48:10 h,Helsinki Runners,FIN,1974,F,W45,10.201,2000011
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,09:57:35 h,Copenhagen Athletics,DNK,1986,F,W35,10.040,2000012
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,10:05:20 h,IF Linnéa,SWE,1981,M,M40,9.912,2000013
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,10:14:45 h,Oslo IL,NOR,1976,M,M45,9.760,2000014
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,10:22:15 h,Helsinki Runners,FIN,1972,M,M50,9.642,2000015
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,10:31:30 h,Copenhagen Athletics,DNK,1984,M,M35,9.501,2000016
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,10:45:05 h,IF Linnéa,SWE,1983,F,W40,9.301,2000017
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,10:55:40 h,Oslo IL,NOR,1978,F,W45,9.151,2000018
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,11:08:25 h,Helsinki Runners,FIN,1985,F,W35,8.976,2000019
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,11:15:50 h,Copenhagen Athletics,DNK,1979,M,M40,8.878,2000020
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,11:27:10 h,IF Linnéa,SWE,1975,M,M45,8.731,2000021
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,11:39:45 h,Oslo IL,NOR,1969,M,M50,8.575,2000022
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,11:51:20 h,Helsinki Runners,FIN,1987,M,M35,8.435,2000023
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,12:04:35 h,Copenhagen Athletics,DNK,1980,F,W40,8.281,2000024
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,12:15:15 h,IF Linnéa,SWE,1974,F,W45,8.160,2000025
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,12:28:40 h,Oslo IL,NOR,1988,F,W35,8.014,2000026
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,12:41:55 h,Helsinki Runners,FIN,1982,M,M40,7.875,2000027
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,12:55:20 h,Copenhagen Athletics,DNK,1977,M,M45,7.739,2000028
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,13:08:45 h,IF Linnéa,SWE,1971,M,M50,7.607,2000029
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,13:22:10 h,Oslo IL,NOR,1986,M,M35,7.480,2000030
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,13:35:35 h,Helsinki Runners,FIN,1981,F,W40,7.357,2000031
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,13:49:00 h,Copenhagen Athletics,DNK,1976,F,W45,7.238,2000032
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,14:03:25 h,IF Linnéa,SWE,1984,F,W35,7.114,2000033
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,14:18:50 h,Oslo IL,NOR,1979,M,M40,6.986,2000034
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,14:32:15 h,Helsinki Runners,FIN,1978,M,M45,6.879,2000035
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,14:47:40 h,Copenhagen Athletics,DNK,1973,M,M50,6.759,2000036
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,15:05:05 h,IF Linnéa,SWE,1985,M,M35,6.629,2000037
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,15:21:30 h,Oslo IL,NOR,1983,F,W40,6.511,2000038
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,15:38:55 h,Helsinki Runners,FIN,1975,F,W45,6.390,2000039
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,15:55:20 h,Copenhagen Athletics,DNK,1987,F,W35,6.281,2000040
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,16:12:45 h,IF Linnéa,SWE,1980,M,M40,6.168,2000041
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,16:35:10 h,Oslo IL,NOR,1974,M,M45,6.029,2000042
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,16:58:35 h,Helsinki Runners,FIN,1970,M,M50,5.890,2000043
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,17:21:00 h,Copenhagen Athletics,DNK,1984,M,M35,5.764,2000044
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,17:45:25 h,IF Linnéa,SWE,1979,F,W40,5.632,2000045
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,18:12:50 h,Oslo IL,NOR,1978,F,W45,5.490,2000046
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,18:45:15 h,Helsinki Runners,FIN,1988,F,W35,5.332,2000047
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,19:18:40 h,Copenhagen Athletics,DNK,1982,M,M40,5.178,2000048
2023,15.03.2023,Stockholm Marathos Ultra (SWE),100km,50,19:55:05 h,IF Linnéa,SWE,1977,M,M45,5.021,2000049"""



OUTPUT_PATH = "/Volumes/marathos/default/raw/stockholm_marathos_ultra_2023.csv"

with open(OUTPUT_PATH, "w") as f:
    f.write(CSV_DATA)

print(f"CSV written to: {OUTPUT_PATH}")

display(spark.sql(f"LIST '/Volumes/marathos/default/raw/'"))