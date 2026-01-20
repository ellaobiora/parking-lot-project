import tkinter as tk
import Vehicle
import ElectricVehicle

# ----------------------------
# Tkinter setup (UI)
# ----------------------------
root = tk.Tk()
root.geometry("650x850")
root.resizable(0, 0)
root.title("Parking Lot Manager")

# Input values (UI state)
num_value = tk.StringVar()
ev_value = tk.StringVar()
make_value = tk.StringVar()
model_value = tk.StringVar()
color_value = tk.StringVar()
reg_value = tk.StringVar()
level_value = tk.StringVar()

ev_car_value = tk.IntVar()      # Electric checkbox (1/0)
ev_car2_value = tk.IntVar()     # Remove EV? checkbox (1/0)
ev_motor_value = tk.IntVar()    # Motorcycle checkbox (1/0)

slot1_value = tk.StringVar()
slot2_value = tk.StringVar()
reg1_value = tk.StringVar()
slot_value = tk.StringVar()

# Output text area
tfield = tk.Text(root, width=70, height=15)


# ----------------------------
# Factory Pattern
# ----------------------------
class VehicleFactory:
    @staticmethod
    def create_vehicle(regnum, make, model, color, ev, motor):
        """
        motor == 1 means Motorcycle (or ElectricBike if EV)
        motor == 0 means Car (or ElectricCar if EV)
        """
        if ev == 1:
            if motor == 1:
                return ElectricVehicle.ElectricBike(regnum, make, model, color)
            return ElectricVehicle.ElectricCar(regnum, make, model, color)

        # Regular vehicle
        if motor == 1:
            return Vehicle.Motorcycle(regnum, make, model, color)
        return Vehicle.Car(regnum, make, model, color)


# ----------------------------
# Domain Model (NO UI COUPLING)
# ----------------------------
class ParkingLot:
    def __init__(self):
        self.capacity = 0
        self.evCapacity = 0
        self.level = 0
        self.numOfOccupiedSlots = 0
        self.numOfOccupiedEvSlots = 0
        self.slots = []
        self.evSlots = []

    def createParkingLot(self, capacity, evcapacity, level):
        self.slots = [-1] * capacity
        self.evSlots = [-1] * evcapacity
        self.level = level
        self.capacity = capacity
        self.evCapacity = evcapacity
        self.numOfOccupiedSlots = 0
        self.numOfOccupiedEvSlots = 0
        return self.level

    def getEmptySlot(self):
        for i in range(len(self.slots)):
            if self.slots[i] == -1:
                return i
        return None

    def getEmptyEvSlot(self):
        for i in range(len(self.evSlots)):
            if self.evSlots[i] == -1:
                return i
        return None

    def park(self, regnum, make, model, color, ev, motor):
        # EV parking
        if ev == 1:
            if self.numOfOccupiedEvSlots >= self.evCapacity:
                return -1

            idx = self.getEmptyEvSlot()
            if idx is None:
                return -1

            self.evSlots[idx] = VehicleFactory.create_vehicle(regnum, make, model, color, ev=1, motor=motor)
            self.numOfOccupiedEvSlots += 1
            return idx + 1  # slot number (1-based)

        # Regular parking
        if self.numOfOccupiedSlots >= self.capacity:
            return -1

        idx = self.getEmptySlot()
        if idx is None:
            return -1

        self.slots[idx] = VehicleFactory.create_vehicle(regnum, make, model, color, ev=0, motor=motor)
        self.numOfOccupiedSlots += 1
        return idx + 1  # slot number (1-based)

    def leave(self, slotid, ev):
        # slotid is 1-based
        index = slotid - 1

        if ev == 1:
            if 0 <= index < len(self.evSlots) and self.evSlots[index] != -1:
                self.evSlots[index] = -1
                self.numOfOccupiedEvSlots -= 1
                return True
            return False

        # regular
        if 0 <= index < len(self.slots) and self.slots[index] != -1:
            self.slots[index] = -1
            self.numOfOccupiedSlots -= 1
            return True
        return False

    # -------- Queries (no UI) --------
    def getRegNumFromColor(self, color):
        regnums = []
        for v in self.slots:
            if v == -1:
                continue
            if v.color == color:
                regnums.append(v.regnum)
        return regnums

    def getSlotNumFromRegNum(self, regnum):
        for i in range(len(self.slots)):
            if self.slots[i] != -1 and self.slots[i].regnum == regnum:
                return i + 1
        return -1

    def getSlotNumFromColor(self, color):
        slotnums = []
        for i in range(len(self.slots)):
            if self.slots[i] == -1:
                continue
            if self.slots[i].color == color:
                slotnums.append(str(i + 1))
        return slotnums

    def getRegNumFromColorEv(self, color):
        regnums = []
        for v in self.evSlots:
            if v == -1:
                continue
            if v.color == color:
                regnums.append(v.regnum)
        return regnums

    def getSlotNumFromRegNumEv(self, regnum):
        for i in range(len(self.evSlots)):
            if self.evSlots[i] != -1 and str(self.evSlots[i].regnum) == str(regnum):
                return i + 1
        return -1

    def getSlotNumFromColorEv(self, color):
        slotnums = []
        for i in range(len(self.evSlots)):
            if self.evSlots[i] == -1:
                continue
            if self.evSlots[i].color == color:
                slotnums.append(str(i + 1))
        return slotnums

    def getSlotNumFromMakeEv(self, make):
        slotnums = []
        for i in range(len(self.evSlots)):
            if self.evSlots[i] == -1:
                continue
            if self.evSlots[i].make == make:
                slotnums.append(str(i + 1))
        return slotnums

    def getSlotNumFromModelEv(self, model):
        slotnums = []
        for i in range(len(self.evSlots)):
            if self.evSlots[i] == -1:
                continue
            if self.evSlots[i].model == model:
                slotnums.append(str(i + 1))
        return slotnums



    def status_text(self):
        output = "Vehicles\nSlot\tFloor\tReg No.\t\tColor\t\tMake\t\tModel\n"
        for i in range(len(self.slots)):
            if self.slots[i] != -1:
                v = self.slots[i]
                output += f"{i+1}\t{self.level}\t{v.regnum}\t\t{v.color}\t\t{v.make}\t\t{v.model}\n"

        output += "\nElectric Vehicles\nSlot\tFloor\tReg No.\t\tColor\t\tMake\t\tModel\n"
        for i in range(len(self.evSlots)):
            if self.evSlots[i] != -1:
                v = self.evSlots[i]
                output += f"{i+1}\t{self.level}\t{v.regnum}\t\t{v.color}\t\t{v.make}\t\t{v.model}\n"

        return output

    def charge_status_text(self):
        output = "Electric Vehicle Charge Levels\nSlot\tFloor\tReg No.\t\tCharge %\n"
        for i in range(len(self.evSlots)):
            if self.evSlots[i] != -1:
                v = self.evSlots[i]
                output += f"{i+1}\t{self.level}\t{v.regnum}\t\t{v.charge}\n"
        return output


# ----------------------------
# Command Pattern (UI actions)
# ----------------------------
class CreateLotCommand:
    def __init__(self, parkinglot):
        self.parkinglot = parkinglot

    def execute(self):
        self.parkinglot.createParkingLot(int(num_value.get()), int(ev_value.get()), int(level_value.get()))
        tfield.insert(tk.INSERT, f"Created a parking lot with {num_value.get()} regular slots and {ev_value.get()} ev slots on level: {level_value.get()}\n")


class ParkCarCommand:
    def __init__(self, parkinglot):
        self.parkinglot = parkinglot

    def execute(self):
        res = self.parkinglot.park(
            reg_value.get(), make_value.get(), model_value.get(), color_value.get(),
            ev_car_value.get(), ev_motor_value.get()
        )
        if res == -1:
            tfield.insert(tk.INSERT, "Sorry, parking lot is full\n")
        else:
            tfield.insert(tk.INSERT, f"Allocated slot number: {res}\n")


class RemoveCarCommand:
    def __init__(self, parkinglot):
        self.parkinglot = parkinglot

    def execute(self):
        status = self.parkinglot.leave(int(slot_value.get()), int(ev_car2_value.get()))
        if status:
            tfield.insert(tk.INSERT, f"Slot number {slot_value.get()} is free\n")
        else:
            tfield.insert(tk.INSERT, f"Unable to remove a car from slot: {slot_value.get()}\n")


class GetSlotByRegCommand:
    def __init__(self, parkinglot):
        self.parkinglot = parkinglot

    def execute(self):
        slot_val = slot1_value.get()
        slotnum = self.parkinglot.getSlotNumFromRegNum(slot_val)
        slotnum2 = self.parkinglot.getSlotNumFromRegNumEv(slot_val)

        if slotnum >= 0:
            tfield.insert(tk.INSERT, f"Identified slot: {slotnum}\n")
        elif slotnum2 >= 0:
            tfield.insert(tk.INSERT, f"Identified slot (EV): {slotnum2}\n")
        else:
            tfield.insert(tk.INSERT, "Not found\n")


class GetSlotByColorCommand:
    def __init__(self, parkinglot):
        self.parkinglot = parkinglot

    def execute(self):
        color = slot2_value.get()
        slotnums = self.parkinglot.getSlotNumFromColor(color)
        slotnums2 = self.parkinglot.getSlotNumFromColorEv(color)

        tfield.insert(tk.INSERT, "Identified slots: " + (", ".join(slotnums) if slotnums else "None") + "\n")
        tfield.insert(tk.INSERT, "Identified slots (EV): " + (", ".join(slotnums2) if slotnums2 else "None") + "\n")


class GetRegByColorCommand:
    def __init__(self, parkinglot):
        self.parkinglot = parkinglot

    def execute(self):
        color = reg1_value.get()
        regnums = self.parkinglot.getRegNumFromColor(color)
        regnums2 = self.parkinglot.getRegNumFromColorEv(color)

        tfield.insert(tk.INSERT, "Registration Numbers: " + (", ".join(regnums) if regnums else "None") + "\n")
        tfield.insert(tk.INSERT, "Registration Numbers (EV): " + (", ".join(regnums2) if regnums2 else "None") + "\n")


class StatusCommand:
    def __init__(self, parkinglot):
        self.parkinglot = parkinglot

    def execute(self):
        tfield.insert(tk.INSERT, self.parkinglot.status_text())


class ChargeStatusCommand:
    def __init__(self, parkinglot):
        self.parkinglot = parkinglot

    def execute(self):
        tfield.insert(tk.INSERT, self.parkinglot.charge_status_text())


# ----------------------------
# Main UI
# ----------------------------
def main():
    parkinglot = ParkingLot()

    # Commands (Command pattern objects)
    create_lot_cmd = CreateLotCommand(parkinglot)
    park_cmd = ParkCarCommand(parkinglot)
    remove_cmd = RemoveCarCommand(parkinglot)
    slot_by_reg_cmd = GetSlotByRegCommand(parkinglot)
    slot_by_color_cmd = GetSlotByColorCommand(parkinglot)
    reg_by_color_cmd = GetRegByColorCommand(parkinglot)
    status_cmd = StatusCommand(parkinglot)
    charge_cmd = ChargeStatusCommand(parkinglot)

    # UI
    label_head = tk.Label(root, text='Parking Lot Manager', font='Arial 14 bold')
    label_head.grid(row=0, column=0, padx=10, columnspan=4)

    label_lot = tk.Label(root, text='Lot Creation', font='Arial 12 bold')
    label_lot.grid(row=1, column=0, padx=10, columnspan=4)

    tk.Label(root, text='Number of Regular Spaces', font='Arial 12').grid(row=2, column=0, padx=5)
    tk.Entry(root, textvariable=num_value, width=6, font='Arial 12').grid(row=2, column=1, padx=4, pady=2)

    tk.Label(root, text='Number of EV Spaces', font='Arial 12').grid(row=2, column=2, padx=5)
    tk.Entry(root, textvariable=ev_value, width=6, font='Arial 12').grid(row=2, column=3, padx=4, pady=4)

    tk.Label(root, text='Floor Level', font='Arial 12').grid(row=3, column=0, padx=5)
    level_entry = tk.Entry(root, textvariable=level_value, width=6, font='Arial 12')
    level_entry.grid(row=3, column=1, padx=4, pady=4)
    level_entry.insert(tk.INSERT, "1")

    tk.Button(
        root, command=create_lot_cmd.execute, text="Create Parking Lot",
        font="Arial 12", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5
    ).grid(row=4, column=0, padx=4, pady=4)

    tk.Label(root, text='Car Management', font='Arial 12 bold').grid(row=5, column=0, padx=10, columnspan=4)

    tk.Label(root, text='Make', font='Arial 12').grid(row=6, column=0, padx=5)
    tk.Entry(root, textvariable=make_value, width=12, font='Arial 12').grid(row=6, column=1, padx=4, pady=4)

    tk.Label(root, text='Model', font='Arial 12').grid(row=6, column=2, padx=5)
    tk.Entry(root, textvariable=model_value, width=12, font='Arial 12').grid(row=6, column=3, padx=4, pady=4)

    tk.Label(root, text='Color', font='Arial 12').grid(row=7, column=0, padx=5)
    tk.Entry(root, textvariable=color_value, width=12, font='Arial 12').grid(row=7, column=1, padx=4, pady=4)

    tk.Label(root, text='Registration #', font='Arial 12').grid(row=7, column=2, padx=5)
    tk.Entry(root, textvariable=reg_value, width=12, font='Arial 12').grid(row=7, column=3, padx=4, pady=4)

    tk.Checkbutton(root, text='Electric', variable=ev_car_value, onvalue=1, offvalue=0, font='Arial 12')\
        .grid(column=0, row=8, padx=4, pady=4)
    tk.Checkbutton(root, text='Motorcycle', variable=ev_motor_value, onvalue=1, offvalue=0, font='Arial 12')\
        .grid(column=1, row=8, padx=4, pady=4)

    tk.Button(
        root, command=park_cmd.execute, text="Park Car",
        font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5
    ).grid(column=0, row=9, padx=4, pady=4)

    tk.Label(root, text='Slot #', font='Arial 12').grid(row=10, column=0, padx=5)
    tk.Entry(root, textvariable=slot_value, width=12, font='Arial 12').grid(row=10, column=1, padx=4, pady=4)

    tk.Checkbutton(root, text='Remove EV?', variable=ev_car2_value, onvalue=1, offvalue=0, font='Arial 12')\
        .grid(column=2, row=10, padx=4, pady=4)

    tk.Button(
        root, command=remove_cmd.execute, text="Remove Car",
        font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5
    ).grid(column=0, row=11, padx=4, pady=4)

    tk.Label(root, text="").grid(row=12, column=0)

    tk.Button(
        root, command=slot_by_reg_cmd.execute, text="Get Slot ID by Registration #",
        font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5
    ).grid(column=0, row=13, padx=4, pady=4)

    tk.Entry(root, textvariable=slot1_value, width=12, font='Arial 12').grid(row=13, column=1, padx=4, pady=4)

    tk.Button(
        root, command=slot_by_color_cmd.execute, text="Get Slot ID by Color",
        font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5
    ).grid(column=2, row=13, padx=4, pady=4)

    tk.Entry(root, textvariable=slot2_value, width=12, font='Arial 12').grid(row=13, column=3, padx=4, pady=4)

    tk.Button(
        root, command=reg_by_color_cmd.execute, text="Get Registration # by Color",
        font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5
    ).grid(column=0, row=14, padx=4, pady=4)

    tk.Entry(root, textvariable=reg1_value, width=12, font='Arial 12').grid(row=14, column=1, padx=4, pady=4)

    tk.Button(
        root, command=charge_cmd.execute, text="EV Charge Status",
        font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5
    ).grid(column=2, row=14, padx=4, pady=4)

    tk.Button(
        root, command=status_cmd.execute, text="Current Lot Status",
        font="Arial 11", bg='PaleGreen1', fg='black', activebackground="PaleGreen3", padx=5, pady=5
    ).grid(column=0, row=15, padx=4, pady=4)

    tfield.grid(column=0, row=16, padx=10, pady=10, columnspan=4)

    root.mainloop()


if __name__ == '__main__':
    main()
