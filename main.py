from utils import *

if __name__ == '__main__':
    data_length = [100000, 10000, 1000, 100, 10]
    container_length = [5, 4, 3, 2, 1]

    for data_len in data_length:
        print("Data Length: {}".format(data_len))
        if os.path.exists("students.csv"):
            os.remove("students.csv")
        generate_student_data(data_len)
        for num_containers in container_length:
            print("Number of Containers: {}".format(num_containers))
            delete_data()
            push_data_thread(num_containers)



