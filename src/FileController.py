class FileController:
    @staticmethod
    def Read_File_Data():
        type = ''
        num_cus = 0
        x = []
        t = []
        with open('../data/A-n32-k5.txt','r') as f:
            for line in f:
                word = line.strip().split(' ')

                if(word[0] == 'NUM_CUS'):
                    type = 'NUM_CUS'
                    continue
                elif(word[0] == 'NODE_COORD_SECTION'):
                    type = 'NODE_COORD_SECTION'
                    continue
                elif(word[0] == 'DEMAND_SECTION'):
                    type = 'DEMAND_SECTION'
                    continue
                elif(word[0] == 'DEPOT_SECTION'):
                    break
                else:
                    if(type == 'NUM_CUS'):
                        num_cus = int(word[0])
                    elif(type == 'NODE_COORD_SECTION'):
                        x.append((float(word[1]),float(word[2])))
                    elif(type == 'DEMAND_SECTION'):
                        t.append(float(word[1]))
        
        return num_cus, x, t

                    

