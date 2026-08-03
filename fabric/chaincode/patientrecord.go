package main

import (
	"encoding/json"
	"fmt"
	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type PatientContract struct {
	contractapi.Contract
}

type Patient struct {
	PatientID    string `json:"patientId"`
	Name         string `json:"name"`
	Age          int    `json:"age"`
	Diagnosis    string `json:"diagnosis"`
	IsRegistered bool   `json:"isRegistered"`
}

func (c *PatientContract) RegisterPatient(ctx contractapi.TransactionContextInterface, patientID string, name string, age int) error {
	exists, err := c.PatientExists(ctx, patientID)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("patient record %s already exists", patientID)
	}

	patient := Patient{
		PatientID:    patientID,
		Name:         name,
		Age:          age,
		Diagnosis:    "",
		IsRegistered: true,
	}

	patientBytes, err := json.Marshal(patient)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(patientID, patientBytes)
}

func (c *PatientContract) UpdateDiagnosis(ctx contractapi.TransactionContextInterface, patientID string, newDiagnosis string) error {
	patientBytes, err := ctx.GetStub().GetState(patientID)
	if err != nil {
		return err
	}
	if patientBytes == nil {
		return fmt.Errorf("patient record %s does not exist", patientID)
	}

	patient := Patient{}
	err = json.Unmarshal(patientBytes, &patient)
	if err != nil {
		return err
	}

	patient.Diagnosis = newDiagnosis
	updatedBytes, err := json.Marshal(patient)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(patientID, updatedBytes)
}

func (c *PatientContract) PatientExists(ctx contractapi.TransactionContextInterface, patientID string) (bool, error) {
	patientBytes, err := ctx.GetStub().GetState(patientID)
	if err != nil {
		return false, err
	}
	return patientBytes != nil, nil
}

func main() {
	cc, err := contractapi.NewChaincode(&PatientContract{})
	if err != nil {
		panic(err)
	}
	if err := cc.Start(); err != nil {
		panic(err)
	}
}
