class FileController:
    @staticmethod
    def Read_File_Data(filename):
        type = ''
        num_cus = 0
        x = []
        t = []
        with open(filename,'r') as f:
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
            f.close()
        return num_cus, x, t

    @staticmethod
    def Read_Multi_File_Data(filenames):
        type = ''
        num_customers = []
        # customers_coord is the coordinate of custumer. The deliver time between 2 person is the distance euclean between them
        customers_coords = []
        # receiving_time is the time what customer receive item
        receiving_times = []
        for filename in filenames:
            num_cus = 0
            x = []
            t = []
            with open(filename,'r') as f:
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
                num_customers.append(num_cus)
                customers_coords.append(x)
                receiving_times.append(t)
                f.close()
        
        return num_customers, customers_coords, receiving_times
                    

