// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title PatientRecord
 * @dev Implementation of Sensitive Healthcare Record Management on Ethereum
 * Identical business logic across Ethereum (Solidity), Corda (Kotlin), and Fabric (Go)
 */
contract PatientRecord {
    struct Patient {
        string patientId;
        string name;
        uint256 age;
        string diagnosis;
        bool isRegistered;
    }

    mapping(string => Patient) private patients;

    event PatientRegistered(string indexed patientId, string name, uint256 age);
    event DiagnosisUpdated(string indexed patientId, string diagnosis);

    function registerPatient(string memory _patientId, string memory _name, uint256 _age) public {
        require(!patients[_patientId].isRegistered, "Patient record already exists");
        patients[_patientId] = Patient(_patientId, _name, _age, "", true);
        emit PatientRegistered(_patientId, _name, _age);
    }

    function updateDiagnosis(string memory _patientId, string memory _diagnosis) public {
        require(patients[_patientId].isRegistered, "Patient record not found or inactive");
        patients[_patientId].diagnosis = _diagnosis;
        emit DiagnosisUpdated(_patientId, _diagnosis);
    }

    function getPatient(string memory _patientId) public view returns (string memory name, uint256 age, string memory diagnosis, bool isRegistered) {
        require(patients[_patientId].isRegistered, "Patient record not found");
        Patient memory p = patients[_patientId];
        return (p.name, p.age, p.diagnosis, p.isRegistered);
    }
}
