import entities  # Asegúrate de que entities.py está en el mismo directorio
import initial_access  # Importamos la clase `Cell` de `initial_access`
import rrc

def main():
    # Create the base station (gNB)
    gnb = entities.gNB()

    # Create Core
    core = entities.Core()

    # Create a UE with supported PLMN IDs and its identity
    ue = entities.UE(supported_plmn_ids=["310260", "40006"], identity="imsi-001010123456789")

    # Add cells to gNB
    gnb.add_cell(initial_access.Cell(cell_id=1, plmn_id="310260", signal_strength=75, frequency=2100, cell_type="Macro"))
    gnb.add_cell(initial_access.Cell(cell_id=2, plmn_id="310260", signal_strength=85, frequency=2600, cell_type="Small"))
    gnb.add_cell(initial_access.Cell(cell_id=3, plmn_id="310560", signal_strength=50, frequency=1800, cell_type="Macro"))

    # Cambiar el "cell_barred" a False en la celda 2, por ejemplo
    gnb.cells[1].cell_barred = False

    # UE searches for available cells
    available_cells = ue.search_cells(gnb.cells)

    # UE selects the best cell based on signal strength
    best_cell = ue.select_cell(available_cells)
    if not best_cell:
        print("No suitable cell found, aborting RRC setup.")
        return

    # Initialize RRC handler
    rrc_handler = rrc.RRC()

    # Simulate the RRC connection request
    rrc_request = rrc_handler.rrc_connection_request(ue)

    # Simulate the RRC connection setup process by gNB
    rrc_response = rrc_handler.rrc_connection_setup(gnb, ue)

    # Complete the RRC connection setup process
    if rrc_handler.rrc_connection_setup_complete(ue) == "RRC_CONNECTED":
        # Explicitly set UE state to "RRC Connected"
        ue.state = "RRC Connected"  # Ensure UE state is set correctly
        print(f"UE state is now: {ue.state}")  # Check if the state was set correctly
        ue.register(core.amf)
    else:
        print("RRC connection setup failed.")
        return

    # Verifying the state before proceeding to the PDU session request
    print(f"Verifying UE state before PDU session request: {ue.state}")
    if ue.state == "RRC Connected":
        print("UE is in RRC Connected state. Proceeding with PDU session establishment.")
        pdu_response = ue.pdu_session_establishment_request(gnb)
        print(f"PDU Session Establishment Response: {pdu_response}")
    else:
        print("Error: UE is not in RRC Connected state, cannot establish PDU session.")
        return

if __name__ == "__main__":
    main()
