import json
import csv

class FileComparison:
    @staticmethod
    def getLinks(filename1, filename2):
        with open(filename1) as json_data:
            data_dict = json.load(json_data)
            # print(data_dict)
            # for x in data_dict:
            #     print(x)
            #     linkList = data_dict.get(x)

        with open(filename2) as json_google:
            google_dict = json.load(json_google)
            #print(google_dict)
            # for y in google_dict:
            #     print(y)
            #     googleList = google_dict.get(y)
        j = 0

        file = open("result.csv", 'w', newline='')
        writer = csv.writer(file)
        writer.writerow(["Queries", "Number of Overlapping Results", "Percent Overlap", "Spearman Coefficient"])

        avg_overlap = 0.0
        avg_percent = 0.0
        avg_spearman = 0.0
        for x, y in zip(data_dict, google_dict):

            linkList = data_dict.get(x)
            googleList = google_dict.get(y)
            #print(linkList)
            overlap, percent, spearman = FileComparison.computeRank(linkList, googleList, j, writer)
            avg_overlap = avg_overlap + overlap
            avg_percent = avg_percent + percent
            avg_spearman = avg_spearman + spearman
            writer.writerow(["Query " + str(j + 1), overlap, percent, spearman])
            j = j + 1
            linkList = []
            googleList = []
        writer.writerow(["Averages", avg_overlap/100, avg_percent/100, avg_spearman/100])
        file.close()
    # read string after https
    def computeRank(l1, l2,j, writer):
        r1 = []
        r2 = []
        i = 0
        for x, xlink in enumerate(l1):
            for y, ylink in enumerate(l2):
                xtemp = xlink.split("//", 1)
                ytemp = ylink.split("//", 1)
                if xtemp[1] == ytemp[1]:
                    r1.append(x+1)
                    r2.append(y+1)

        # Spearman Coefficient
        d2 = []
        for i in range(len(r2)):
            d = r2[i] - r1[i]
            d2.append(d*d)
        d2_sum = sum(d2)
        #print(d_sum)
        #print(d2_sum)
        n = len(r2)
        if n <= 1:
            spearman = 0
        else:
            num = (6.0*d2_sum)
            den = (n*((n*n)-1))
            spearman = 1.0 - (num / den)
        # Overlap percent with Google
        #print(spearman)
        #spearmanA = []
        #spearmanA.append(spearman)

        #overlap = []
        overlap = len(r2)

        #percent = []
        percent = (len(r2)/len(l2))*100

        #with open("result.csv", 'w', newline='') as file:
        #    writer = csv.writer(file)
        #    writer.writerow(["Queries", "Number of Overlapping Results", "Percent Overlap", "Spearman Coefficient"])
            #for j in range(len(l1)):
        return overlap, percent, spearman

#calculate Average



FileComparison.getLinks("searchResult.json","googleResult.json")
