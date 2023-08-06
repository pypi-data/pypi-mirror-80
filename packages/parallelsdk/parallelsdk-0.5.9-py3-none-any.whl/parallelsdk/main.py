import os
import random
import numpy as np

from parallelsdk.data_toolbox.data_toolbox import *
from parallelsdk.mp_toolbox.mp_toolbox import *
from parallelsdk.mp_toolbox.mp_model import *
from parallelsdk.routing_toolbox.routing_toolbox import *
from parallelsdk.cp_toolbox.cp_toolbox import *
from parallelsdk.scheduling_toolbox.SchedulingModels.Employee import Employee
from parallelsdk.scheduling_toolbox.SchedulingModels.Staff import Staff
from parallelsdk.scheduling_toolbox.scheduling_toolbox import *
from parallelsdk.deployment.deployment_model import *
from parallelsdk.client import *
from parallelsdk.test.smart_grid_cp_model import *

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def createVRPModel(vrp):
    np.random.seed(1)
    depot_loc = np.random.uniform(0.0, 10.0, size=(2,))
    vrp.AddDepot(depot_loc)
    delivery_loc = []
    for k in range(10):
        delivery = np.random.uniform(0.0, 10.0, size=(2,))
        delivery_loc.append(delivery)
        vrp.AddLocation(position=delivery, demand=random.randint(5, 10))

    # vrp.AddVehicle( name="vehicle_%d" %(1), load=0.0, capacity=300)
    for k in range(3):
        vrp.AddVehicle(name="vehicle_%d" % k, load=0.0, capacity=5)
    vrp.InferDistanceMatrix()
    return vrp


def createMappedVRPModel(vrp):
    vrp.AddDepot("145 Concord Rd Wayland, MA 01778")
    vrp.AddLocation("13 Lincoln Rd Wayland, MA 01778", demand=random.randint(5, 10), location_id=1)
    vrp.AddLocation("662 Boston Post Rd, Weston, MA 02493", demand=random.randint(5, 10), location_id=2)
    vrp.AddLocation("2345 Commonwealth Avenue, Newton, MA 02466", demand=random.randint(5, 10), location_id=3)
    vrp.AddLocation("180 Hemenway Rd, Framingham, MA 01701", demand=random.randint(5, 10), location_id=4)
    vrp.AddLocation("72 Wayside Inn Rd, Sudbury, MA 01776", demand=random.randint(5, 10), location_id=5)
    vrp.AddLocation("22 Flutie Pass, Framingham, MA 01701", demand=random.randint(5, 10), location_id=6)
    vrp.AddLocation("208 S Great Rd, Lincoln, MA 01773", demand=random.randint(5, 10), location_id=7)
    vrp.AddLocation("9 Hope Ave, Waltham, MA 02453", demand=random.randint(5, 10), location_id=8)
    vrp.InferDistanceMatrix(metric='maps', API_key='AIzaSyCGOa79k466MIwCERz5_obRhmONuebj5Cs')

    for k in range(3):
        vrp.AddVehicle(name="vehicle_%d" % k, load=0.0, capacity=30)

    return vrp


def createSchedulingModel(scheduler):
    model = scheduler.get_instance()
    team = Staff("Team", "575.123.4567", "TruckBest")
    mario = Employee("Mario", "M", "587.234.1543", "TruckBest", "Boston")
    john = Employee("John", "M", "878.232.5873", "TruckBest", "Boston")
    team.add_staff_member(mario, 100)
    team.add_staff_member(john, 100)
    team.add_shift_preference(1, 0, 10)
    model.set_schedule_num_days(5)
    model.set_shift_per_day(3)
    model.add_staff(team)


def createMPModel(model):
    inf = Infinity()
    x = model.IntVar(0.0, inf, 'x')
    y = model.IntVar(0.0, inf, 'y')
    # print(x)
    # print(y)
    c1 = model.Constraint(x + 7 * y <= 17.5)
    c2 = model.Constraint(x <= 3.5)
    model.Objective(x + 10 * y, maximize=True)


def createJobShopModel(job_shop):
    js = job_shop.get_instance()
    js.set_search_timeout(10.0)
    js.set_num_parallel_cores(1)
    machine_1 = js.add_machine(1)
    machine_1.add_time_window_availability(32, 54)
    job_1 = js.add_job(1)
    job_1.add_dependency(machine_1.get_id())
    task_1 = job_1.add_task()
    task_1.set_required_machine(machine_1.get_id())
    task_1.set_duration(10)


def createCPModel(model):
    x = model.IntVar(0, 10, 'x')
    y = model.IntVar(0, 10, 'y')
    print(x.to_string())
    print(y.to_string())
    # model.Constraint(x != y)
    c = model.AllDifferent([x, y])
    print(c.to_string())
    model.set_objective(y, minimize=False)


def createPythonFunctionTool(tool):
    python_fcn = tool.get_instance()
    python_fcn.add_entry_fcn_name("myFcn")
    python_fcn.add_entry_module_name("my_file")
    python_fcn.add_input_argument(3, "int")
    python_fcn.add_input_argument([3.14, 4.15], "double")
    python_fcn.clear_input_arguments()
    python_fcn.add_input_argument(5)
    python_fcn.add_input_argument(6)
    python_fcn.add_output_argument("int", False)
    python_fcn.add_output_argument("bool", True)

    # Add the path to the test folder
    path_str = str(os.path.join(os.path.dirname(__file__), "test"))
    python_fcn.add_environment_path(path_str)
    return tool


def runConnection(optimizer):
    print("Connecting...")
    optimizer.connect()

    model = input("Run model [r(routing)/s(scheduling)/m(mp)/d(data)/c(cp)/p(deploy)/j(job-shop)/n(none)]: ")
    if model == "n":
        pass
    elif model == "r":
        vrp = createMappedVRPModel(BuildVRP('example'))
        optimizer.run_optimizer_synch(vrp)
        solution = vrp.get_solution()
        for route in solution:
            print("Route: " + str(route.get_route()))
            print("Total distance: " + str(route.get_total_distance()))
    elif model == "d":
        data_tool = createPythonFunctionTool(BuildPythonFunctionTool("fcn_tool"))
        optimizer.run_optimizer_synch(data_tool)
        output = data_tool.get_instance().get_output()
        print(output)
    elif model == "p":
        deployment = DeploymentModel()
        deployment.deploy_model("abc")
        optimizer.run_optimizer_synch(deployment)
    elif model == "c":
        cp = CPModel('cp_model')
        # createCPModel(cp.get_model())
        createSmartGridCPModel(cp.get_model())
        optimizer.run_optimizer_synch(cp)
        solution = cp.get_model().get_solution()
        print(solution)
    elif model == "j":
        js = BuildJobShopScheduler("job_shop")
        createJobShopModel(js)
        optimizer.run_optimizer_synch(js)
        jobs = js.get_instance().get_all_jobs()
        print(js.get_instance().get_model_status())
        for job in jobs:
            print(job)
        js.get_instance().print_solution()
    elif model == "s":
        scheduler = BuildEmployeesScheduler('test')
        createSchedulingModel(scheduler)
        optimizer.run_optimizer_synch(scheduler)
    else:
        pass

    val = input("Disconnect? [Y/N]: ")
    optimizer.disconnect()


def main():
    #vrp = BuildVRP('example')
    #depot = vrp.AddDepot('145+Concord+Rd+Wayland+MA')
    #depot.get_coordinates(API_key="AIzaSyCGOa79k466MIwCERz5_obRhmONuebj5Cs")
    #return

    # cp = CPModel('cp_model')
    # createSmartGridCPModel(cp.get_model())
    # return

    mp = MPModel('mip_example')
    createMPModel(mp)

    data_tool = BuildPythonFunctionTool("fcn_tool")
    createPythonFunctionTool(data_tool)

    js = BuildJobShopScheduler("job_shop")
    createJobShopModel(js)

    print("Create a client...")
    optimizer = ParallelClient('127.0.0.1')
    val = input("Connect to back-end [Y/N]: ")
    if val == 'Y':
        runConnection(optimizer)


if __name__ == '__main__':
    main()
