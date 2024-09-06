import tkinter as tk
from tkinter import messagebox
import numpy as np
import next_screen as ns
import pandas as pdD

#필요한 변수 초기화
room_space_R = 0
room_space_C = 0
space = []
distance_sensor_loc = [(0, room_space_C), (room_space_R, 0), (room_space_R, room_space_C)]
furniture_activity_dict = {'empty':['']}  # 가구와 활동 딕셔너리
furniture_list_dict = {0: 'empty'}  # 가구와 고유번호 딕셔너리

def create_furniture_list(): #숫자와 가구명 연결한 리스트 생성/반복되는 과정 함수화
    furniture_list_dict = {0: 'empty'}  # 재생성을 위한 초기화
    furniture_list_dict2=furniture_activity_dict.keys()
    furniture_list=list(furniture_list_dict2)
    
    for i in range(1, len(furniture_list)):
        furniture_list_dict[i]= furniture_list[i] 
    ns.furniture_list_dict_ns = furniture_list_dict
    return furniture_list_dict

def delete_screen(root):  #창 닫는 함수
    root.destroy()

def open_room_size_screen():  #메인 함수
    def get_room_size():  #방 크기를 입력받는 함수
        global room_space_R, room_space_C, space
        room_space_C = int(width_entry.get())
        room_space_R = int(height_entry.get())

        if room_space_C <= 0 or room_space_R <= 0:
            root.withdraw()
            tk.messagebox.showerror("오류", "가로와 세로 길이는 양의 정수이어야 합니다.")
            root.deiconify()
        else:
            print("가로 길이:", room_space_C, "cm")
            print("세로 길이:", room_space_R, "cm")
            space = np.zeros((room_space_R, room_space_C))
            ns.space_ns = space
            ns.room_space_C_ns = room_space_C
            ns.room_space_R_ns = room_space_R
            ns.distance_sensor_loc_ns = [(0, ns.room_space_C_ns), (ns.room_space_R_ns, 0), (ns.room_space_R_ns, ns.room_space_C_ns)]
            root.destroy()
            open_space_info_screen()  # 공간 정보 입력 화면으로 이동

    root = tk.Tk()
    root.title("방 크기 입력")
    root.geometry("400x200")

    title_label = tk.Label(root, text="방의 가로와 세로 길이를 입력하세요\n[10cm단위로 입력할것]", font=("Arial", 16))
    title_label.pack(pady=10)
    
    explain_label = tk.Label(root, text="문과 가장 가까운 모서리를 (0,0)으로 가정할 것", font=("Arial", 10), fg="gray")
    explain_label.pack(pady=5)

    frame = tk.Frame(root)
    frame.pack(pady=5)

    width_label = tk.Label(frame, text="가로 길이(10cm):")
    width_label.grid(row=0, column=0)

    width_entry = tk.Entry(frame, width=10)
    width_entry.grid(row=0, column=1)

    height_label = tk.Label(frame, text="세로 길이(10cm):")
    height_label.grid(row=1, column=0)

    height_entry = tk.Entry(frame, width=10)
    height_entry.grid(row=1, column=1)

    confirm_button = tk.Button(root, text="확인", command=get_room_size, width=10)
    confirm_button.pack(pady=10)

    root.mainloop()

def open_space_info_screen():  #첫 화면 생성 함수
    root = tk.Tk()
    root.title("공간 정보 입력")
    root.geometry("400x450")

    def exit_app(): #프로그램 종료 함수
        print("Exit action initiated")
        root.quit()
        root.destroy()
        exit()

    title_label = tk.Label(root, text="공간 정보 입력", font=("Arial", 24))
    title_label.pack(pady=20)

    button1 = tk.Button(root, text="1-1.가구 추가", command=activity_each_furniture, width=15, height=2)
    button1.pack(pady=5) 

    button2 = tk.Button(root, text="1-2가구 삭제", command=delete_furniture, width=15, height=2)
    button2.pack(pady=5)

    button3 = tk.Button(root, text="2.가구 배치", command=set_furniture, width=15, height=2)
    button3.pack(pady=5)

    button4 = tk.Button(root, text="3-1.가구 배치 현황", command=display_array, width=15, height=2)
    button4.pack(pady=5)

    button5 = tk.Button(root, text="3-2배치 초기화", command=reset_furniture, width=15, height=2)
    button5.pack(pady=5)

    button6 = tk.Button(root, text="다음", command=lambda:ns.next_screen(root), width=15, height=2)  
    button6.pack(pady=5)

    button7 = tk.Button(root, text="종료", command=exit_app, width=10, height=1)  
    button7.pack(pady=5)

    root.mainloop()
    


def activity_each_furniture():  #가구와 그 가구에서의 활동 입력
    ns.activity_each_furniture_check=True #activity_each_furniture함수 작동 여부 확인
    
    def go_back():  #되돌아가기 버튼 함수
        delete_screen(root)
    def add_activity():  #입력받은 내용 딕셔너리에 저장
        global furniture_list_dict
        try:
            name = name_entry.get()
            activity = activity_entry.get()

            if name.strip() and activity.strip():
                if name in furniture_activity_dict:
                    furniture_activity_dict[name].append(activity)
                else:
                    furniture_activity_dict[name] = [activity]
                furniture_list_dict=create_furniture_list() #furniture_list_dict 업데이트          
                ns.furniture_activity_dict_ns = furniture_activity_dict  #next_screen에도 전달
                activity_entry.delete(0, tk.END)
            else:
                raise ValueError("가구 종류와 활동 내용을 모두 입력하세요.")
        except ValueError as e:
            root.withdraw()
            tk.messagebox.showerror("오류", str(e))
            root.deiconify()
        except Exception as e:
            root.withdraw()
            tk.messagebox.showerror("예상치 못한 오류 발생", str(e))
            root.deiconify()

    root = tk.Tk()
    root.title("가구 활동 입력")
    root.geometry("350x180")

    title_label = tk.Label(root, text="가구 종류와 활동 내용을 입력하세요", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    name_frame = tk.Frame(root)
    name_frame.grid(row=1, column=0, columnspan=2, pady=5)

    name_label = tk.Label(name_frame, text="가구 종류:")
    name_label.grid(row=0, column=0)

    name_entry = tk.Entry(name_frame, width=20)
    name_entry.grid(row=0, column=1)

    activity_frame = tk.Frame(root)
    activity_frame.grid(row=2, column=0, columnspan=2, pady=5)

    activity_label = tk.Label(activity_frame, text="활동 내용:")
    activity_label.grid(row=0, column=0)

    activity_entry = tk.Entry(activity_frame, width=20)
    activity_entry.grid(row=0, column=1)

    confirm_button = tk.Button(root, text="추가", command=add_activity, width=10)
    confirm_button.grid(row=3, column=0, padx=5, pady=10)
    
    back_button = tk.Button(root, text="돌아가기", command=go_back, width=10)
    back_button.grid(row=3, column=1, padx=5, pady=10)

    root.mainloop()

def set_furniture():  #가구 배치하는 함수
    furniture_list_dict=create_furniture_list()
    temp_furniture_list_dict=furniture_list_dict.copy()
    del temp_furniture_list_dict[0]  #가구목록 출력을 위해 기본값 제거

    def go_back():
        delete_screen(root)
        
    def add_furniture():  #가구id와 크기, 위치를 입력받음
        try:
            furniture_id = int(furniture_entry.get())
            furniture_C, furniture_R = map(int, size_entry.get().split('*'))
            furniture_loc_C, furniture_loc_R = map(int, location_entry.get().split('*'))

            if furniture_id not in temp_furniture_list_dict:
                raise ValueError("잘못된 가구 ID입니다.")

            for a in range(furniture_loc_R, furniture_loc_R + furniture_R):  #해당 위치의 배열에 가구id 입력
                for b in range(furniture_loc_C, furniture_loc_C + furniture_C):
                    space[a][b] = furniture_id

            furniture_entry.delete(0, tk.END)  
            size_entry.delete(0, tk.END)
            location_entry.delete(0, tk.END)
            ns.space_ns = space  #next_screen에도 업데이트된 space전달
            
        except ValueError as e:
            root.withdraw()
            tk.messagebox.showerror("오류", "목록을 확인하세요\n"+str(e))
            root.deiconify()
        except Exception as e:
            root.withdraw()
            tk.messagebox.showerror("예상치 못한 오류 발생", str(e))
            root.deiconify()

        
        
    root = tk.Tk()
    root.title("가구 배치")
    root.geometry("280x300")

    title_label = tk.Label(root, text="가구 배치", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    furniture_frame = tk.Frame(root)
    furniture_frame.grid(row=1, column=0, columnspan=2, pady=5)
    
    furniture_label = tk.Label(furniture_frame, text=temp_furniture_list_dict)
    furniture_label.grid(row=0, column=0, columnspan=2, pady=10)
    
    furniture_label = tk.Label(furniture_frame, text="해당 번호 입력:")
    furniture_label.grid(row=1, column=0, padx=(0, 5), sticky="e")

    furniture_entry = tk.Entry(furniture_frame, width=20)
    furniture_entry.grid(row=1, column=1, sticky="w")

    size_frame = tk.Frame(root)
    size_frame.grid(row=2, column=0, columnspan=2, pady=5)

    size_label = tk.Label(size_frame, text="가구 크기(10cm*10cm):")
    size_label.grid(row=0, column=0, padx=(0, 5), sticky="e")

    size_entry = tk.Entry(size_frame, width=20)
    size_entry.grid(row=0, column=1, sticky="w")

    location_frame = tk.Frame(root)
    location_frame.grid(row=3, column=0, columnspan=2, pady=5)

    location_label = tk.Label(location_frame, text="가구 위치(10cm*10cm):")
    location_label.grid(row=0, column=0, padx=(0, 5), sticky="e")

    location_entry = tk.Entry(location_frame, width=20)
    location_entry.grid(row=0, column=1, sticky="w")

    add_button = tk.Button(root, text="추가", command=add_furniture, width=10)
    add_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    back_button = tk.Button(root, text="돌아가기", command=go_back, width=10)
    back_button.grid(row=5, column=0, columnspan=2, pady=10)

    root.mainloop()

def delete_furniture():  #입력받은 가구 삭제 함수
    global furniture_list_dict, furniture_activity_dict
    furniture_list_dict=create_furniture_list()
    temp_furniture_list_dict=furniture_list_dict.copy()
    del temp_furniture_list_dict[0]
    
    def go_back():
        delete_screen(root)
    def delete():  #가구명을 받으면 furniture_activity_dict에서 삭제
        global furniture_activity_dict
        try:
            temp = furniture_entry.get()
            if temp in furniture_activity_dict:
                del furniture_activity_dict[temp]
                ns.furniture_activity_dict_ns = furniture_activity_dict  #next_screen에도 업데이트된 furniture_activity_dict전달
                furniture_entry.delete(0, tk.END)
            else:
                raise ValueError("가구 '{}'를 찾을 수 없습니다.".format(temp))
            reset_furniture()  #가구 수정됨에 따라 배치도 초기화
            
        except ValueError as e:
            root.withdraw()
            tk.messagebox.showerror("오류", str(e))
            root.deiconify()
        except Exception as e:
            root.withdraw()
            tk.messagebox.showerror("예상치 못한 오류 발생", str(e))
            root.deiconify()
            

    root = tk.Tk()
    root.title("가구 삭제")
    root.geometry("350x280")

    title_label = tk.Label(root, text="삭제하고 싶은 가구를 입력하세요", font=("Arial", 16))
    title_label.pack(pady=10)

    furniture_frame = tk.Frame(root)
    furniture_frame.pack(pady=5)

    furniture_list_label = tk.Label(furniture_frame, text=temp_furniture_list_dict)
    furniture_list_label.grid(row=0, column=0, columnspan=2, pady=10)

    furniture_label = tk.Label(furniture_frame, text="가구 이름:")
    furniture_label.grid(row=1, column=0)

    furniture_entry = tk.Entry(furniture_frame, width=20)
    furniture_entry.grid(row=1, column=1)
    
    guide_label = tk.Label(root, text="주의:가구 배치가 초기화 됩니다", font=("Arial", 10), fg="gray")
    guide_label.pack(pady=5)

    delete_button = tk.Button(root, text="삭제", command=delete, width=10)
    delete_button.pack(pady=10)
    
    back_button = tk.Button(root, text="돌아가기", command=go_back, width=10)
    back_button.pack(pady=10)

    root.mainloop()

def reset_furniture():  #전체 배열값 0으로 초기화
    def show_popup():
        messagebox.showinfo("안내", "가구 배치가 초기화 되었습니다.")
    for a in range(room_space_R):
        for b in range(room_space_C):
            space[a][b]=0
    ns.space_ns = space
    show_popup()

def display_array():  #배열의 값에 따라 색상을 넣어 출력
    furniture_list_dict=create_furniture_list()
    temp_furniture_list_dict=furniture_list_dict.copy()
    del temp_furniture_list_dict[0]
    
    colors = [
    "black", "red", "blue", "green", "yellow", "orange",
    "purple", "magenta", "cyan", "lime", "pink",
    "gold", "tomato", "deepskyblue", "darkorange", "springgreen",
    "violet", "darkred", "navy", "hotpink", "chartreuse"
    ]

    try:
        root = tk.Tk()
        root.title("공간 지도")

        title_label = tk.Label(root, text=temp_furniture_list_dict, font=("Arial", 16))
        title_label.pack(pady=10)
        subtitle_label = tk.Label(root, text=colors[1:len(temp_furniture_list_dict)+1], font=("Arial", 16))  #각 가구의 색상 종류도 출력
        subtitle_label.pack(pady=10)

        canvas = tk.Canvas(root)
        scrollbar_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollbar_y.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar_x = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        canvas.pack(side="top", fill="both", expand=True)

        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        rows = len(space)
        cols = len(space[0])
        for i in range(rows):
            for j in range(cols):           
                label = tk.Label(frame, text=str(space[i][j]), font=("Arial", 10), borderwidth=1, relief="solid", width=5, height=2, fg=colors[int(space[i][j])])  #각 배열값으로 가구 종류 파악 후 색상 부여하여 출력
                label.grid(row=i, column=j)

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        root.mainloop()
    
    except TypeError:
        root.withdraw()
        messagebox.showerror("에러", "관리자에게 문의하세요.")
        root.deiconify()
        
# 프로그램 시작
open_room_size_screen()