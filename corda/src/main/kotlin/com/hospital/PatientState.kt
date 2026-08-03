package com.hospital

import net.corda.core.contracts.BelongsToContract
import net.corda.core.contracts.ContractState
import net.corda.core.contracts.LinearState
import net.corda.core.contracts.UniqueIdentifier
import net.corda.core.identity.AbstractParty
import net.corda.core.identity.Party

/**
 * R3 Corda State Implementation for Healthcare Record Management.
 * Implements LinearState for UTXO state consumption and issuance.
 */
@BelongsToContract(PatientContract::class)
data class PatientState(
    val patientId: String,
    val name: String,
    val age: Int,
    val diagnosis: String,
    val status: String,
    val hospital: Party,
    val physician: Party,
    override val linearId: UniqueIdentifier = UniqueIdentifier(patientId)
) : LinearState {
    override val participants: List<AbstractParty> get() = listOf(hospital, physician)
}
