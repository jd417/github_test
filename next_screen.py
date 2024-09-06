import tkinter as tk
import csv
from tkinter import filedialog
import threading
import time
from datetime import datetime

# 전역 변수로 Schedule_list와 stop_event 선언
Schedule_list = []
stop_event = threading.Event()

#필요한 변수 초기화
activity_each_furniture_check=False
distances = [21, 28, 28]  # 리스트 형식으로 장치로부터 거리정보 입력받음/ 현재는 임의로 부여
room_space_R_ns = 0
room_space_C_ns = 0
distance_sensor_loc_ns = [(0, room_space_C_ns), (room_space_R_ns, 0), (room_space_R_ns, room_space_C_ns)]
furniture_activity_dict_ns = []
furniture_list_dict_ns = [] 
space_ns = []
Now_schedule = ''

def trilaterate(distances, points):  #삼각측량법 함수
    # 입력값을 언패킹하여 좌표와 거리를 추출합니다.
    point1, point2, point3 = points
    distance1, distance2, distance3 = distances
    
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    # 세 지점으로부터의 거리를 이용하여 위치를 계산합니다.
    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    C = 2 * (x3 - x1)
    D = 2 * (y3 - y1)
    
    E = distance1**2 - distance2**2 - x1**2 + x2**2 - y1**2 + y2**2
    F = distance1**2 - distance3**2 - x1**2 + x3**2 - y1**2 + y3**2
    
    # 위치 계산에 사용할 행렬을 구성합니다.
    try:
        x = (E * D - B * F) / (A * D - B * C)
        y = (A * F - E * C) / (A * D - B * C)
        x_int = int(x)
        y_int = int(y)
        return x_int, y_int
    except ZeroDivisionError:
        tk.messagebox.showerror("오류", "위치를 계산할 수 없습니다. 센서를 확인 후 관리자에게 문의하세요")
        return None

def next_screen(previous_screen):
    previous_screen.withdraw()
    
    def go_back2():  #되돌아가기 버튼 함수
        delete_screen(root)
        previous_screen.deiconify()
    def delete_screen(root):  #창 닫는 함수
        root.destroy()

    def on_button1_click():
        global Schedule_list
        try:
            # CSV 파일 선택 창 열기
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if file_path:
                # CSV 파일을 처리하는 함수 호출
                Schedule_list = process_csv(file_path)
        except Exception as e:
            tk.messagebox.showerror("오류", "일정표 양식을 확인하세요\n"+str(e))
        
    def on_button2_click():
        root.withdraw() #기존 창 숨김           
        
        # 새로운 창 생성
        control_window = tk.Toplevel()
        control_window.title("감시 중")
        control_window.geometry("400x230")

        def Assess_action(PC_Data, SMARTPHONE_Data, SMARTWATCH_Data, Various_Devices_Data):  # pc, 스마트폰, 웨어러블 디바이스 등을 통해 움직임이나 수면상태, 실행 중인 프로그램 등 정보를 받아 현재 위치에서의 활동 리스트에서 사용자의 활동을 최종 판단하는 함수
            global furniture_list_dict_ns, furniture_activity_dict_ns, space_ns
            result = trilaterate(distances, distance_sensor_loc_ns)
            # 구현 실패로 함수 내용 없음
            return(furniture_activity_dict_ns[furniture_list_dict_ns[int(space_ns[result[0]][result[1]])]][0])  # 각 가구의 첫번째 활동으로 행동 부여
    
        def compare():  #일정 수행 여부 판단 함수
            global Now_schedule, text
            try:
                Real_action = Assess_action("PC", "SMARTPHONE", "SMARTWATCH", "Various_Devices")
                Now_action = Now_schedule
                if Real_action != Now_action:
                    text = "정신차려라!!"
                    tk.messagebox.showerror("오류", str(text))
                elif Real_action == Now_action:
                    text = "일정 수행 중"
                elif Real_action == "":  #일정이 없는 경우
                    text = "-일정 없음-"
            except Exception as e:
                tk.messagebox.showerror("오류", str(e))
            return text

        def start_action():
            global Schedule_list, stop_event, Now_schedule
            stop_event.clear()  # stop_event 재설정, 중지 기능 구현을 위함

            while not stop_event.is_set():
                try:
                    # 오늘 요일 가져오기 (0: 월요일, 1: 화요일, ..., 6: 일요일)
                    current_time = datetime.now()
                    today_weekday = current_time.weekday()
                    current_date = current_time.date()

                    Now_schedule = ''  #현재 일정 초기화
                    for i in range(len(Schedule_list[today_weekday])):
                        Std = Schedule_list[today_weekday][i][0]  #일정 시작 시간
                        Ftd = Schedule_list[today_weekday][i][1]  #일정 종료 시간

                        Sstd = datetime.strptime(str(current_date) + " " + Std, "%Y-%m-%d %H:%M")  #비교를 위해 양식 변경
                        Fstd = datetime.strptime(str(current_date) + " " + Ftd, "%Y-%m-%d %H:%M")

                        if Sstd <= current_time <= Fstd:  #현재 일정 분류
                            Now_schedule = Schedule_list[today_weekday][i][2]
                            break

                    if Now_schedule == '':
                        Now_schedule = ''

                    new_message = compare()
                    label.config(text=new_message)  #비교 결과 출력위해 텍스트 변경

                except KeyError as e:
                    print(f"키 오류: {e}")
                    label.config(text="키 오류가 발생했습니다.")
                except IndexError as e:
                    print(f"인덱스 오류: {e}")
                    label.config(text="일정을 확인하세요")
                except ValueError as e:
                    print(f"값 오류: {e}")
                    label.config(text="값 오류가 발생했습니다.")
                except Exception as e:
                    print(f"예기치 못한 오류: {e}")
                    label.config(text="예기치 못한 오류가 발생했습니다.")
                time.sleep(1)  # 1초 마다 반복하여 수행 여부 판단

        def stop_action():  #관리 중지 함수
            global stop_event
            label.config(text="중지")
            stop_event.set()  # stop_event 설정

        def go_back():  #되돌아가기 함수
            control_window.destroy()
            root.deiconify()

        def exit_app():  #프로그램 종료 함수
            root.quit()
            root.destroy()
            exit()

        label = tk.Label(control_window, text="감시 시작")
        label.pack(pady=5)

        start_button = tk.Button(control_window, text="실행", command=lambda: threading.Thread(target=start_action).start(), width=20, height=2)
        start_button.pack(pady=5)

        stop_button = tk.Button(control_window, text="중지", command=stop_action, width=20, height=2)
        stop_button.pack(pady=5)

        back_button = tk.Button(control_window, text="돌아가기", command=go_back, width=20, height=2)
        back_button.pack(pady=5)

        exit_button = tk.Button(control_window, text="종료", command=exit_app, width=10, height=1)
        exit_button.pack(pady=5)

    def process_csv(file_path):  #csv파일로 일정표를 입력받아 list로 처리하는 함수
        def read_csv_file(file_path):
            data = []
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    data.append(row)
            return data

        csv_data = read_csv_file(file_path)

        Schedule_list = []
        day_list2 = []
        n = 1

        while True:
            while True:
                exe_list = []
                
                for i in range(1, 4):
                    exe_list.append(csv_data[n][i])
                n += 1
                day_list2.append(exe_list)
                if csv_data[n][0] != '':
                    break

            if csv_data[n][0] == 'end' and csv_data[n][1] == 'end':
                Schedule_list.append(day_list2)
                break
            elif csv_data[n][0] != 'end':
                Schedule_list.append(day_list2)
                day_list2 = []
                
        return Schedule_list

    root = tk.Tk()
    root.title("감시 준비")
    root.geometry("400x230")

    if activity_each_furniture_check == False:
        root.withdraw()
        tk.messagebox.showerror("오류", "가구를 추가하세요")
        go_back2()

    def exit_app():
            print("Exit action initiated")
            root.quit()
            root.destroy()
            exit()

    button1 = tk.Button(root, text="일정 입력", command=on_button1_click, width=20, height=2)
    button1.pack(pady=5)

    button2 = tk.Button(root, text="관리 시작", command=on_button2_click, width=20, height=2)
    button2.pack(pady=5)
    
    back_button = tk.Button(root, text="돌아가기", command=go_back2, width=20, height=2)
    back_button.pack(pady=5)
    
    button3 = tk.Button(root, text="종료", command=exit_app, width=10, height=1)
    button3.pack(pady=5)
    
    root.mainloop()

