import random

class AUSF:
    def authenticate(self, ue_identity, udm):
        # AUSF authenticates UE with the help of UDM (Unified Data Management)
        print(f"AUSF: Authenticating UE identity: {ue_identity}")
        return {"authenticated": udm.authenticate(ue_identity), "algorithm": "5G-AKA"}

class UDM:
    def __init__(self):
        # Stores subscriber data for authentication
        self.subscriber_data = {"imsi-001010123456789", "imsi-001310123456789"}

    def authenticate(self, ue_identity):
        # UDM authenticates the UE using IMSI (International Mobile Subscriber Identity)
        print(f"UDM: Authenticating UE {ue_identity}")
        if ue_identity in self.subscriber_data:
            return True
        else:
            return False

    def register_ue(self, ue_identity):
        # Registers the UE after successful authentication
        print(f"UDM: UE registered: {ue_identity}")
    
    def get_subscription_data(self, ue_identity):
        # Retrieves subscription data for the UE
        print(f"UDM: Subscription data retrieved for UE: {ue_identity}")

class gNB:
    def __init__(self):
        self.cells = []  # gNB manages a list of cells
        self.state = "Idle"

    def add_cell(self, cell):
        """Add a cell to the gNB"""
        self.cells.append(cell)

    def process_rrc_connection_request(self, ue):
        """Simulate gNB receiving the RRC connection request and sending setup"""
        print(f"gNB: Processing RRC connection request from UE with selected cell ID: {ue.selected_cell.cell_id}...")
        setup_data = {
            "plmn_id": ue.selected_cell.plmn_id,
            "cell_id": ue.selected_cell.cell_id,
            "signal_strength": ue.selected_cell.signal_strength,
            "frequency": ue.selected_cell.frequency,
            "network_configuration": "Configured for high-speed data"
        }
        self.state = "RRC Connection Setup Sent"
        return setup_data
    
    def rrc_connection_setup_complete(self, ue):
        """Simulate gNB completing the RRC connection setup"""
        print(f"gNB: Sending RRC connection setup to UE with configuration: {ue.selected_cell.frequency} Hz")
        ue.rrc_connection_setup_complete()

class Core:
    def __init__(self):
        self.amf = AMF()  # Core initializes the AMF (Access and Mobility Management Function) for the network

class AMF:
    def __init__(self):
        self.ausf = AUSF()  # AMF interacts with AUSF (Authentication Server Function) for authentication
        self.udm = UDM()    # AMF communicates with UDM (Unified Data Management) for subscription data

    def receive_registration_request(self, ue_identity):
        # AMF receives registration request from UE and triggers authentication
        print(f"AMF: Received REGISTRATION REQUEST from UE with identity: {ue_identity}")
        return self.authenticate(ue_identity)

    def authenticate(self, ue_identity):
        # AMF initiates authentication through AUSF and UDM
        print(f"AMF: Initiating authentication with AUSF...")
        auth_data = self.ausf.authenticate(ue_identity, self.udm)
        if auth_data["authenticated"]:
            print(f"AMF: Authentication successful for UE: {ue_identity}")
            print("AMF: Sending SECURITY MODE COMMAND...")
            print("UE: SECURITY MODE COMPLETE received.")
            print("AMF: Requesting PEI from UE...")
            print("UE: Sending IDENTITY RESPONSE with PEI.")
            print("AMF: Checking PEI with 5G-EIR... (skipped)")
            print("AMF: Registering with UDM...")
            self.udm.register_ue(ue_identity)
            print("AMF: Getting subscription data from UDM...")
            self.udm.get_subscription_data(ue_identity)
            print("AMF: Sending REGISTRATION ACCEPT to UE...")
            print("UE: REGISTRATION COMPLETE sent.")
            return True
        else:
            print(f"AMF: Authentication failed for UE: {ue_identity}")
            return False

    def process_pdu_session_request(self, ue):
        """ Handle the PDU Session Establishment Request sent by UE to the Core """
        print(f"AMF: Processing PDU Session Establishment Request from UE with identity: {ue.identity}")
        # Verify if UE is registered
        if ue.rm_state == "RM-REGISTERED":
            print(f"AMF: PDU session request validated for UE: {ue.identity}")
            # PDU session establishment handled directly in the Core
            return "PDU Session Established"
        else:
            print(f"AMF: UE is not registered, cannot process PDU session request.")
            return "PDU Session Establishment Failed"

class UE:
    def __init__(self, supported_plmn_ids, identity):
        self.supported_plmn_ids = supported_plmn_ids
        self.state = "Idle"
        self.selected_cell = None
        self.rm_state = "RM-DEGISTERED"  # Registration state is initially "DEGISTERED"
        self.identity = identity

    def pdu_session_establishment_request(self, core):
        """Simulate UE sending PDU Session Establishment Request to AMF (Core)"""
        print(f"UE: Sending PDU Session Establishment Request to AMF...")
        return core.amf.process_pdu_session_request(self)

    def search_cells(self, available_cells):
        """Simulate the UE searching for available cells"""
        print("UE: Searching for available cells...")
        return available_cells
    
    def select_cell(self, cells):
        """Select the best cell based on signal strength"""
        valid_cells = []

        for cell in cells:
            mib = cell.send_mib()
            sib = cell.send_sib()
            if mib["plmn_id"] in self.supported_plmn_ids:
                valid_cells.append((cell, mib, sib))
        
        if not valid_cells:
            print("No suitable cell found. Search failed.")
            return None

        # Choose the best cell based on signal strength
        best_cell, best_mib, best_sib = max(valid_cells, key=lambda x: x[0].signal_strength)
        self.selected_cell = best_cell
        print(f"UE: Selected Cell ID: {best_cell.cell_id}, Signal Strength: {best_cell.signal_strength}, Frequency: {best_cell.frequency}, PLMN ID: {best_cell.plmn_id}, Cell Type: {best_sib['cell_type']}")
        return best_cell

    def rrc_connection_request(self):
        """Simulate UE sending RRC connection request with additional details"""
        print(f"UE: Sending RRC connection request to gNB...")
        request_data = {
            "plmn_id": self.selected_cell.plmn_id,
            "cell_id": self.selected_cell.cell_id,
            "signal_strength": self.selected_cell.signal_strength,
            "frequency": self.selected_cell.frequency
        }
        self.state = "RRC Connection Request Sent"
        return request_data
    
    def rrc_connection_setup_complete(self):
        """Simulate UE completing the RRC connection setup"""
        print(f"UE: Received RRC connection setup response and completed setup.")
        self.state = "RRC Connected"
        return "RRC Connection Setup Complete"
    
    def register(self, amf):
        # Send registration request to AMF (Access and Mobility Management Function)
        print(f"UE: Sending REGISTRATION REQUEST to AMF with identity: {self.identity}")
        if amf.receive_registration_request(self.identity):
            self.state = "RRC Connected"  # Ensure the state is "RRC Connected"
            self.rm_state = "RM-REGISTERED"  # Change state to "RM-REGISTERED"
            print(f"UE state after registration: {self.state}")
        else:
            print(f"UE: with identity: {self.identity} not authenticated")

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
