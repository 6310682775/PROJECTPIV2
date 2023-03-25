from celery import shared_task
from detect_and_track import mymain
from main.models import Task, LoopResult, VehicleCount
import os


@shared_task
def run_detect(vdofile, loopfile, task_id):
    saved_result = mymain(loopfile, cmd=False, custom_arg=[
                          '--source', vdofile])
    task = Task.objects.get(pk=task_id)
    counting_result_path, video_result_path = saved_result
    counting_result_file = open(counting_result_path, 'rb')
    video_file = open(video_result_path, 'rb')
    task.video_result_file.save(f"{task_id}.mp4", video_file, save=True)
    task.counting_result_file.save(
        f"{task_id}.txt", counting_result_file, save=True)
    task.save()
    counting_result_file.close()
    video_file.close()
    all_loop = []

    # loops = Loop.objects.filter(head_task__pk=task_id)
    loop_count = 3
    for i in range(loop_count):
        vehicle_counts = {
            "Bus": {"ENTERED": 0, "STRAIGHT": 0, "RIGHT": 0, "LEFT": 0},
            "Car": {"ENTERED": 0, "STRAIGHT": 0, "RIGHT": 0, "LEFT": 0},
            "Container truck": {"ENTERED": 0, "STRAIGHT": 0, "RIGHT": 0, "LEFT": 0},
            "Motorcycle sidecar": {"ENTERED": 0, "STRAIGHT": 0, "RIGHT": 0, "LEFT": 0},
            "Motorcycle": {"ENTERED": 0, "STRAIGHT": 0, "RIGHT": 0, "LEFT": 0},
            "Pickup truck": {"ENTERED": 0, "STRAIGHT": 0, "RIGHT": 0, "LEFT": 0},
            "Trailer truck": {"ENTERED": 0, "STRAIGHT": 0, "RIGHT": 0, "LEFT": 0},
            "Truck": {"ENTERED": 0, "STRAIGHT": 0, "RIGHT": 0, "LEFT": 0},
            "Tuktuk": {"ENTERED": 0, "STRAIGHT": 0, "RIGHT": 0, "LEFT": 0},
            "Van": {"ENTERED": 0, "STRAIGHT": 0, "RIGHT": 0, "LEFT": 0}
        }
        all_loop.append(vehicle_counts)

    path = f"media/result/counting/{task_id}.txt"
    with open(path, 'r') as f:
        data = f.readlines()

    for line in data:
        field = line.strip().split(",")
        field[-1] = field[-1].replace(" ", "")
        for i in range(loop_count):
            if (field[0] == str(i)):
                vehicle_type = field[2]
                direction = field[4]
                all_loop[i][vehicle_type][direction] += 1

    task = Task.objects.get(pk=task_id)

    for i in range(loop_count):
        loop_result = LoopResult.objects.create(
            task_loop_result=task, loop_id=i)
        vehicles = ["Bus", "Car", "Container truck", "Motorcycle sidecar",
                    "Motorcycle", "Pickup truck", "Trailer truck", "Truck", "Tuktuk", "Van"]
        for car_type in vehicles:
            vehicle_count = VehicleCount.objects.create(loop_result=loop_result, loop_id=i, vehicle_type=car_type, entered=all_loop[i][car_type][
                                                        "ENTERED"], straight=all_loop[i][car_type]["STRAIGHT"], right=all_loop[i][car_type]["RIGHT"], left=all_loop[i][car_type]["LEFT"])
            vehicle_count.save()
        loop_result.save()

    for loop_id in range(loop_count):
        folder_path = f"summary/result/{task_id}/"

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        csv_data = "vehicle_type,entered,straight,right,left\n"
        for key, value in all_loop[loop_id].items():
            row = [key] + list(value.values())
            csv_data += ",".join(map(str, row)) + "\n"

        save_csv_path = f"{folder_path}/{task_id}_{loop_id}.csv"
        # Save CSV string to text file
        with open(save_csv_path, "w") as f:
            f.write(csv_data)

        folder_path_upload = f"media/result/summary/{task_id}/"

        if not os.path.exists(folder_path):
            os.makedirs(folder_path_upload)
        loop_result = LoopResult.objects.get(
            task_loop_result__task_id=task_id, loop_id=loop_id)

        csv_file = open(save_csv_path, 'rb')
        loop_result.summary_file.save(
            f"{task_id}/{task_id}_{loop_id}.csv", csv_file, save=True)

        loop_result.save()
    return saved_result


def save_result_to_task(saved_result, task_id):
    task = Task.objects.get(pk=task_id)
    counting_result_path, video_result_path = saved_result
    counting_result_file = open(counting_result_path, 'rb')
    video_file = open(video_result_path, 'rb')
    task.video_result_file.save(f"{task_id}.mp4", video_file, save=True)
    task.counting_result_file.save(
        f"{task_id}.txt", counting_result_file, save=True)
    task.save()
    counting_result_file.close()
    video_file.close()
