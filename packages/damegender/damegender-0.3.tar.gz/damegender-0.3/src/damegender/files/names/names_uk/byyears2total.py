#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2020  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Damegender; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, 
# Boston, MA 02110-1301 USA,

# create a file with name and prob from uk births
total = 0
for i in range(1880, 2018):
    # first we acquire the total of births from 1880 to 2017
    dataset = "orig/yob" + str(i) + ".txt"
    with open(dataset) as csvfile:
        sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(sexreader, None)
        totali = 0
        for row in sexreader:
            datasetcount = row[2]
            totali = totali + int(datasetcount)
            total = total + totali

# now we are going to start the json file with 1880
jsonuk = "orig/jsonuk.json"
file = open(jsonuk, "w")
dataset = "orig/yob1880.txt"
with open(dataset) as csvfile:
    sexreader1 = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(sexreader1, None)
    cnt = 0
    for row in sexreader1:
        cnt = cnt + 1
        end = cnt
        lines = []
        lines.append('[')
        
with open(dataset) as csvfile:
    sexreader2 = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(sexreader2, None)
    cnt = 1
    for row in sexreader2:
        lines.append('{"name": "' + row[0] + '",')
        lines.append('"gender": "' + row[1] + '",')
        if (end == cnt):
            lines.append('"count": ' + row[2] + '}')
            print('"count": ' + row[2] + '}')
        else:
            lines.append('"count": ' + row[2] + '},')
            print('"count": ' + row[2] + '},')
            cnt = cnt + 1
            lines.append(']')
            fo = open(jsonuk, "w")
            fo.writelines(lines)
            # Cerramos el archivo
            
for i in range(1881, 2018):
    dataset = "orig/yob" + str(i) + ".txt"
    with open(dataset) as csvfile:
        sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(sexreader, None)
        lines = []
        for row in sexreader:
            print(row)
            #         Cerramos el archivo
fo.close()
