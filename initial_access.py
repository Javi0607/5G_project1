import random
import time

class Cell:
    def __init__(self, cell_id, signal_strength, plmn_id, frequency, cell_type):
        self.cell_id = cell_id
        self.signal_strength = signal_strength
        self.plmn_id = plmn_id
        self.frequency = frequency  # New property for frequency
        self.cell_type = cell_type  # New property for cell type
    
    def send_mib(self):
        # Simulate sending MIB (Master Information Block)
        mib = {
            "cell_id": self.cell_id,
            "plmn_id": self.plmn_id,
            "bandwidth": random.choice([10, 20, 40, 80, 100]),
            "scheduling_info": random.randint(1, 10)
        }
        print(f"Cell {self.cell_id} sent MIB: {mib}")
        return mib
    
    def send_sib(self):
        # Simulate sending SIB (System Information Block)
        sib = {
            "plmn_id": self.plmn_id,
            "tracking_area_code": random.randint(1, 1000),
            "cell_barred": random.choice([True, False]),
            "allowed_access_classes": list(range(1, 11)),
            "cell_type": self.cell_type  
        }
        print(f"Cell {self.cell_id} sent SIB: {sib}")
        return sib
