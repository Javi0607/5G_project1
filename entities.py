import random

class Cell:
    def __init__(self, cell_id, signal_strength, plmn_id, frequency, cell_type):
        self.cell_id = cell_id  # Unique identifier for the cell
        self.signal_strength = signal_strength  # Signal strength in dBm
        self.plmn_id = plmn_id  # PLMN (Public Land Mobile Network) identifier
        self.frequency = frequency  # Frequency at which the cell operates
        self.cell_type = cell_type  # Type of the cell (Macro, Small, etc.)
    
    def send_mib(self):
        """ Simulate sending the Master Information Block (MIB) with cell parameters """
        mib = {
            "cell_id": self.cell_id,
            "plmn_id": self.plmn_id,
            "bandwidth": random.choice([10, 20, 40, 80, 100]),  # Bandwidth options
            "scheduling_info": random.randint(1, 10)  # Scheduling information for the cell
        }
        return mib
    
    def send_sib(self):
        """ Simulate sending the System Information Block (SIB) """
        sib = {
            "plmn_id": self.plmn_id,
            "tracking_area_code": random.randint(1, 1000),  # Tracking area code
            "cell_barred": random.choice([True, False]),  # Whether the cell is barred
            "allowed_access_classes": list(range(1, 11)),  # Allowed access classes for the cell
            "cell_type": self.cell_type  # Type of the cell
        }
        return sib


class UE:
    def __init__(self, supported_plmn_ids, identity):
        self.supported_plmn_ids = supported_plmn_ids  # PLMN IDs supported by the UE
        self.state = "Idle"  # Initial state of the UE
        self.selected_cell = None  # Cell selected by the UE
        self.rm_state = "RM-DEGISTERED"  # Registration state
        self.identity = identity  # Identity of the UE (e.g., IMSI)

    def pdu_session_establishment_request(self, core):
        """ Simulate the PDU Session Establishment Request sent to the AMF """
        print(f"\n---[PDU Session Establishment Request]---")
        print(f"UE: Sending PDU Session Establishment Request to AMF with PDU Session ID and location information...")
        return core.amf.process_pdu_session_request(self)

    def search_cells(self, available_cells):
        """ Simulate the UE searching for available cells """
        print("UE: Searching for available cells...")
        return available_cells
    
    def select_cell(self, cells):
        """ Simulate the UE selecting the best cell based on signal strength """
        valid_cells = []
        for cell in cells:
            mib = cell.send_mib()
            sib = cell.send_sib()
            if mib["plmn_id"] in self.supported_plmn_ids:
                valid_cells.append((cell, mib, sib))
        
        if not valid_cells:
            print("No suitable cell found. Search failed.")
            return None

        best_cell, best_mib, best_sib = max(valid_cells, key=lambda x: x[0].signal_strength)
        self.selected_cell = best_cell
        print(f"\nUE: Selected Cell ID: {best_cell.cell_id}, Signal Strength: {best_cell.signal_strength}, Frequency: {best_cell.frequency}, PLMN ID: {best_cell.plmn_id}, Cell Type: {best_sib['cell_type']}")
        return best_cell

    def rrc_connection_request(self):
        """ Simulate the UE sending an RRC connection request to the gNB """
        print(f"\n---[RRC Connection Request]---")
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
        """ Simulate the UE completing the RRC connection setup """
        print(f"\n---[RRC Connection Setup Complete]---")
        print(f"UE: Received RRC connection setup response and completed setup.")
        self.state = "RRC Connected"
        return "RRC Connection Setup Complete"
    
    def register(self, amf):
        """ Simulate the UE sending a registration request to the AMF """
        print(f"\n---[UE Registration]---")
        print(f"UE: Sending REGISTRATION REQUEST to AMF with identity: {self.identity}")
        if amf.receive_registration_request(self.identity):
            self.state = "RRC Connected"
            self.rm_state = "RM-REGISTERED"
            print(f"UE state after registration: {self.state}")
        else:
            print(f"UE: with identity: {self.identity} not authenticated")

class gNB:
    def __init__(self):
        self.cells = []  # List of cells managed by the gNB
        self.state = "Idle"  # Initial state of the gNB

    def add_cell(self, cell):
        """ Add a cell to the gNB's list of cells """
        self.cells.append(cell)

    def process_rrc_connection_request(self, ue):
        """ Process the RRC connection request from the UE """
        print(f"\n---[gNB RRC Processing]---")
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
        """ Complete the RRC connection setup and update UE state """
        print(f"\ngNB: Sending RRC connection setup to UE with configuration: {ue.selected_cell.frequency} Hz")
        ue.rrc_connection_setup_complete()

class Core:
    def __init__(self):
        self.amf = AMF()  # AMF is the main function for handling registration and session establishment

class AMF:
    def __init__(self):
        self.ausf = AUSF()  # Authentication Server Function
        self.udm = UDM()  # Unified Data Management function

    def receive_registration_request(self, ue_identity):
        """ AMF receives a registration request from the UE """
        print(f"\n---[AMF Registration]---")
        print(f"AMF: Received REGISTRATION REQUEST from UE with identity: {ue_identity}")
        return self.authenticate(ue_identity)

    def authenticate(self, ue_identity):
        """ Initiates authentication using AUSF and UDM """
        print(f"AMF: Initiating authentication with AUSF...")
        auth_data = self.ausf.authenticate(ue_identity, self.udm)
        if auth_data["authenticated"]:
            print(f"AMF: Authentication successful for UE: {ue_identity}")
            return True
        else:
            print(f"AMF: Authentication failed for UE: {ue_identity}")
            return False

    def process_pdu_session_request(self, ue):
        """ Process the PDU session establishment request sent by UE """
        print(f"\n---[PDU Session Request]---")
        print(f"AMF: Processing PDU Session Establishment Request from UE with identity: {ue.identity}")
        if ue.rm_state == "RM-REGISTERED":
            print(f"AMF: PDU session request validated for UE: {ue.identity}")
            # Assign the "Client Anchor" (UPF) for managing the data session
            print("AMF: Assigning Client Anchor (UPF) for PDU session.")
            return "PDU Session Established"
        else:
            print(f"AMF: UE is not registered, cannot process PDU session request.")
            return "PDU Session Establishment Failed"

class AUSF:
    def authenticate(self, ue_identity, udm):
        """ Authenticate UE using the UDM """
        print(f"AUSF: Authenticating UE identity: {ue_identity}")
        return {"authenticated": udm.authenticate(ue_identity), "algorithm": "5G-AKA"}

class UDM:
    def __init__(self):
        self.subscriber_data = {"imsi-001010123456789", "imsi-001310123456789"}  # Example subscriber data

    def authenticate(self, ue_identity):
        """ Authenticate the UE based on IMSI """
        print(f"UDM: Authenticating UE {ue_identity}")
        if ue_identity in self.subscriber_data:
            return True
        else:
            return False

    def register_ue(self, ue_identity):
        """ Register the UE in the system """
        print(f"UDM: UE registered: {ue_identity}")
    
    def get_subscription_data(self, ue_identity):
        """ Retrieve subscription data for the UE """
        print(f"UDM: Subscription data retrieved for UE: {ue_identity}")

class UPF:
    def __init__(self, name):
        self.name = name
    
    def establish_tunnel(self, client_upf):
        """ Establish an N4-based tunnel with the Client UPF """
        print(f"Anchor UPF: Establishing N4-based tunnel with {client_upf.name} (Client UPF).")
        return f"Tunnel established between {self.name} and {client_upf.name}"
    
    def send_tunnel_info(self, smf):
        """ Send tunnel information to the SMF """
        print(f"{self.name}: Sending tunnel information to SMF.")
        smf.receive_tunnel_info(self.name)

class SMF:
    def __init__(self):
        self.upf = UPF("Anchor UPF")  # Anchor UPF for handling the data session

    def receive_tunnel_info(self, upf_name):
        """ Receive tunnel information from the UPF """
        print(f"SMF: Received tunnel info from {upf_name}.")
    
    def process_pdu_session(self, ue):
        """ Process the PDU session and establish the session with the UPF """
        print("\n---[PDU Session Establishment]---")
        print("SMF: Processing PDU session for UE...")
        # Link with UPF (Client Anchor and Anchor UPF)
        client_upf = UPF("Client UPF")
        tunnel_info = self.upf.establish_tunnel(client_upf)
        print(f"SMF: {tunnel_info}")
        self.upf.send_tunnel_info(self)
        print(f"SMF: PDU session successfully established for UE: {ue.identity}")
