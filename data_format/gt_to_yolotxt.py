input_train_path = "E:\\workspace\\YOLOv3\\data\\FullIJCNN2013_jpg\\gt.txt"
output_train_path = "E:\\workspace\\YOLOv3\\data\\FullIJCNN2013_jpg\\"
orign_w =1360
orign_h = 800
def get_label(label):
    prohibitory = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 15, 16]  # (circular, white ground with red border)
    mandatory = [33, 34, 35, 36, 37, 38, 39, 40]  # (circular, blue ground)
    danger = [11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]  # (triangular, white ground with red border)
 
    if label in prohibitory:
        new_label = "0"
    elif label in mandatory:
        new_label = "1"
    elif label in danger:
        new_label = "2"
    else:
        new_label = "3"
 
    return new_label
#read origin txt transform to coco
def gt2yolo():
    file_name=''
    for line in open(input_train_path,"r"):  # 设置文件对象
        # line = f.readline().strip()
        # while line :
            words = line.split(';')
            img_name= words[0].split(".")[0]
            label = get_label(int(words[-1]))
            x = float(words[1]) /orign_w
            w = float(words[3])/ orign_w -x
            y = float(words[2]) / orign_h
            h = float(words[4]) / orign_h - y
            #save
            if output_train_path+img_name+".txt" != file_name:
                file_name = output_train_path+img_name+".txt"
                fw = open(file_name, 'w')
            else:
                fw = open(file_name, 'a')
            fw.write(label+" "+str(x) + " " + str(y) + " "+ str(w) + " "+ str(h) + "\n")
            fw.close()
 
if __name__ == '__main__':
    gt2yolo()
    print("transform finsih")
