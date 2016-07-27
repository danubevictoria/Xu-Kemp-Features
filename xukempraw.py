'''
Created on Jul 5, 2012

@author: Danube Phan
'''
import re;

def readFeatureData():
    """
    In xukemp.txt: 
    A1-A19: from xukempfinal data
    A20-A53: from xukempnegations data
    B1-B171: pairwise conjunctions for xukempfinal
    B172-B732: pairwise conjunctions for xukempnegations
    C1-C969: 3-way conjunctions for xukempfinal
    C970-C6953: 3-way conjunctions for xukempnegations
    D1-D3876: 4-way conjunctions for xukempfinal
    D3877-D50252: 4-way conjunctions for xukempnegations
    Read scenes from feature sets from xukemp.txt into a dictionary. 
    """
    scenes = {} #empty dict
    f = open('xukemp.txt', 'r')
    for line in f:
        words = line.split()
        if (len(words) != 0): #if line is not empty
            #print re.search('[a-zA-Z]', words[0]);
            if (re.search('[a-zA-Z]', words[0]) != 'None'): #check if first word in line is a feature label ex. A1
                feature = words[0]; #ex. A1
                labelNum = int(words[0][1:]); #ex. A1 <- 1 is the label number
                scenes.setdefault(labelNum, {}).setdefault(feature, []); #insert label number as key to feature label with empty list for values contained within feature
                i = 1; #i is for indexing through words in the line
            else:
                i = 0;
            if (len(words) > 1):
                scene = words[i];
                #for all scenes up to the last scene in a feature set, 
                #insert it into dict under correct label number and feature label
                while((scene != words[-1]) & (re.search('[a-zA-Z]', scene) != 'None')):
                    scenes[labelNum][feature].append(int(scene));  
                    i = i + 1;  
                    scene = words[i];
                    scenes[labelNum][feature].append(int(scene));
    f.close()
    return scenes;

def writeConjB(db, start, end, begLabelNum):
    '''
    Creates conjunctions that must be formed from exactly 2 unique features with only label A. 
    Conjunctions cannot be made from any of the same feature set.
    Ex. A1 ^ A1 NOT ALLOWED; A1 by itself NOT ALLOWED; A1 ^ A2 ^ A3 NOT ALLOWED; 
    B1 ^ A1 NOT ALLOWED
    Duplicate conjunctions involving the same parent features are NOT stored. 
    Ex. If A1 ^ A2 was already stored, then A2 ^ A1 NOT STORED
    But conjunctions with duplicate contents and differing parents are stored.
    Ex. A1^A2 = [1, 2, 3, 4] STORED; A1^A3 = [1, 2, 3, 4] STORED
    Assign the valid conjunctions with label B.
    Append to end of file: xukemp.txt along with parents features of that conjunction.
    Ex. Features A1, A2, A3, A4
    Valid Conjunctions: A1 ^ A2, A1 ^ A3, A1 ^ A4, A2 ^ A3, A2 ^ A4, A3 ^ A4
    '''
    print "working..."
    labelNum = begLabelNum; #for creating new labels with B; ex. B1 <- 1 is labelNum
    # find conjunction between all unique pairs of features
    for i in range(start, end):
        feature1 = set(db[i]['A' + str(i)]);
        for j in range(i+1, end+1):
            feature2 = set(db[j]['A' + str(j)]);
            conjunction = sorted(list(feature1 & feature2));
            #append to xukemp.txt with new labels B
            with open("xukemp.txt", "a") as myfile:
                label = "B" + str(labelNum) + " ";
                myfile.write(label);
                parents = "A" + str(i) + "A" + str(j) + " ";
                myfile.write(parents);
                for scene in conjunction:
                    myfile.write(str(scene) + " ");
                myfile.write("\n");
            labelNum = labelNum + 1;
    print "done writing conj B!"

def writeConjC(db, start, end, begLabelNum):
    '''
    Create conjunctions using exactly 3 unique feature sets with only label A.
    Conjunctions cannot be made from any of the same feature sets.
    Ex. A1 ^ A1 ^ A1 NOT ALLOWED; A1 by itself NOT ALLOWED; 
    A1 ^ A2 ^ A2 NOT ALLOWED; B1 ^ A1 ^ A2 NOT ALLOWED; A1 ^ A2 NOT ALLOWED;
    A1 ^ A2 ^ A3 ^ A4 NOT ALLOWED
    Duplicate conjunctions involving the same parent features are NOT stored. 
    Ex. If A1 ^ A2 ^ A3 was already stored, then A2 ^ A1 ^ A3 NOT STORED
    But conjunctions with duplicate contents and differing parents are stored.
    Ex. A1^A2^A3 = [1, 2, 3, 4] STORED; A1^A3^A4 = [1, 2, 3, 4] STORED
    Assign the valid conjunctions with label C.
    Append to end of file: xukemp.txt along with parents features of that conjunction.
    Ex. Features A1, A2, A3, A4
    Valid Conjunctions: A1 ^ A2 ^ A3, A1 ^ A2 ^ A4, A1 ^ A3 ^ A4
    '''
    print "working...";
    labelNum = begLabelNum; #for creating new labels with B; ex. B1 <- 1 is labelNum
    for i in range(start, end-1):
        feature1 = set(db[i]['A' + str(i)]);
        for j in range(i+1, end):
            feature2 = set(db[j]['A' + str(j)]);
            for k in range(j+1, end+1):
                feature3 = set(db[k]['A' + str(k)]);
                conjunction = sorted(list(feature1 & feature2 & feature3));
                with open("xukemp.txt", "a") as myfile:
                    label = "C" + str(labelNum) + " ";
                    myfile.write(label);
                    parents = "A" + str(i) + "A" + str(j) + "A" + str(k) + " ";
                    myfile.write(parents);
                    for scene in conjunction:
                        myfile.write(str(scene) + " ");
                    myfile.write("\n");
                labelNum = labelNum + 1;
    print "done writing conj C!";
                
def writeConjD(db, start, end, begLabelNum):
    '''
    Create conjunctions using exactly 4 unique feature sets with only label A.
    Conjunctions cannot be made from any of the same feature sets.
    Ex. A1 ^ A1 ^ A1 ^ A1 NOT ALLOWED; A1 by itself NOT ALLOWED; 
    A1 ^ A2 ^ A2 ^ A3 NOT ALLOWED; B1 ^ A1 ^ A2 ^ B2 NOT ALLOWED; A1 ^ A2 NOT ALLOWED;
    A1 ^ A2 ^ A3 ^ A4 ^ A5 NOT ALLOWED
    Duplicate conjunctions involving the same parent features are NOT stored.  
    Ex. If A1 ^ A2 ^ A3 ^ A4 was already stored, then A2 ^ A1 ^ A3 ^ A4 NOT STORED
    But conjunctions with duplicate contents and differing parents are stored.
    Ex. A1^A2^A3^A4 = [1, 2, 3, 4] STORED; A1^A3^A4^A5 = [1, 2, 3, 4] STORED
    Assign the valid conjunctions with label D.
    Append to end of file: xukemp.txt along with parents features of that conjunction.
    Ex. Features A1, A2, A3, A4, A5
    Valid Conjunctions: A1 ^ A2 ^ A3 ^ A4, A1 ^ A2 ^ A3 ^ A5, A1 ^ A3 ^ A4 ^ A5
    '''
    print "working..."
    labelNum = begLabelNum; #for creating new labels with B; ex. B1 <- 1 is labelNum
    for i in range(start, end-2):
        feature1 = set(db[i]['A' + str(i)]);
        for j in range(i+1, end-1):
            feature2 = set(db[j]['A' + str(j)]);
            for k in range(j+1, end):
                feature3 = set(db[k]['A' + str(k)]);
                for l in range(k+1, end+1):
                    feature4 = set(db[l]['A' + str(l)]);
                    conjunction = sorted(list(feature1 & feature2 & feature3 & feature4));
                    with open("xukemp.txt", "a") as myfile:
                        label = "D" + str(labelNum) + " ";
                        myfile.write(label);
                        parents = "A" + str(i) + "A" + str(j) + "A" + str(k) + "A" + str(l) + " ";
                        myfile.write(parents);
                        for scene in conjunction:
                            myfile.write(str(scene) + " ");
                        myfile.write("\n");
                    labelNum = labelNum + 1;
    print "done writing conj D!"

#--- main program
db = readFeatureData();
writeConjB(db, 1, 19, 1);
writeConjB(db, 20, 53, 172);
writeConjC(db, 1, 19, 1);
writeConjC(db, 20, 53, 970);
writeConjD(db, 1, 19, 1);
writeConjD(db, 20, 53, 3877);