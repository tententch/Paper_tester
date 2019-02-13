import cv2
from matplotlib import pyplot as plt

ref_photo = "more/ref.jpg"
input_photo = "more/ref.jpg"

Percent_effi_g = 0.01/100;
Percent_effi_s = 0.05/100;
Percent_effi_b = 0.1/100;

Percent_effi = [Percent_effi_g,Percent_effi_s,Percent_effi_b];  


def crop_img(input_photo):
    img = cv2.imread(input_photo, cv2.IMREAD_COLOR)
    crop_img = img[270:700, 150:450];
    plt.imshow(crop_img);
    return crop_img;

def crop_ref_img(input_photo):
    img = cv2.imread(input_photo, cv2.IMREAD_COLOR)
    crop_img = img[270:700, 150:450];
    plt.imshow(crop_img);
    return crop_img;


def ref_paper(img):
    ref_white_num = 0;
    plt.imshow(img);
    histogram = cv2.calcHist([img], [0], None, [256], [0, 256]);
    max_value = max(histogram);

    for j in range(len(histogram)):
        if max_value == histogram[j]:
            ref_white_num = max_value;
            ref_white_num = ref_white_num[0];
            color = j;

            plt.figure()
            plt.title("Reference_Paper")
            plt.xlabel("grayscale value")
            plt.ylabel("pixels")
            plt.xlim([-2, 255])

            plt.plot(histogram)
            plt.show()
      
            print("White num of ref_paper = ",ref_white_num);
            print("max histrogram is = ",color);
            return ref_white_num,color;


def input_P(img):
    plt.imshow(img)
    histogram = cv2.calcHist([img], [0], None, [256], [0, 256]);
    white_paper = 0;
    
    plt.figure()
    plt.title("Input_Paper")
    plt.xlabel("grayscale value")
    plt.ylabel("pixels")
    plt.xlim([-2, 255])

    plt.plot(histogram)
    plt.show()
    
    for i in range(10):
        white_paper += histogram[i+246];
    if white_paper > 700000:
        decision=1;
    else: 
        decision=0;
    
    return decision;
    
    
def effi_check(img,ref_white_num,Percent_effi,decision,color,decision2):
    histogram = cv2.calcHist([img], [0], None, [256], [0, 256])
    
    expect_Gold_White_num = ref_white_num-(Percent_effi[0]*(ref_white_num))
    expect_Silver_White_num = ref_white_num-(Percent_effi[1]*(ref_white_num))
    expect_Broze_White_num = ref_white_num-(Percent_effi[2]*(ref_white_num))
    
    max_value = max(histogram);
    
    print('Expect for gold   = more than %d' %expect_Gold_White_num)
    print('Expect for silver = more than %d' %expect_Silver_White_num)
    print('Expect for bronze = more than %d' %expect_Broze_White_num)
    print(" ")
    
    for k in range(len(histogram)):
        if max_value == histogram[k]:
            input_white_num = max_value;
            input_white_num = input_white_num[0];
            color = k;
    
    if decision == 1 and decision2 == 1:
       print('Input_White_Num = %d' %histogram[color])
       if histogram[color] >= expect_Gold_White_num:
           print("'Gold Grade'");
       elif histogram[color] >= expect_Silver_White_num:
           print("'Silver Grarde'");
       elif histogram[color] >= expect_Broze_White_num:
           print("'Bronze Grade'");
       else:
           print("'Can not use'");
    else:
       print(" ")
       print('Input_White_Num = %d' %histogram[color])
       print(" ");
       print("'Can not use'");

def size_check(img):
    decision2=1;
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    ret,thresh = cv2.threshold(img,100,256,0);
    im2,contours,hierarchy = cv2.findContours(thresh, 1, 2)
    all_object = [];
    for item in range(len(contours)):
        cnt = contours[item]
        all_object = len(cnt)
        if all_object >= 5:
            decision2=0;
            return decision2;
        else:
            decision2=1;
    return decision2;


crop_img = crop_img(input_photo);
crop_ref_img = crop_ref_img(ref_photo);
ref_paper = ref_paper(crop_ref_img);
input_P = input_P(crop_img);
size_check = size_check(crop_img);
effi_check(crop_img,ref_paper[0],Percent_effi,input_P,ref_paper[1],size_check);




    