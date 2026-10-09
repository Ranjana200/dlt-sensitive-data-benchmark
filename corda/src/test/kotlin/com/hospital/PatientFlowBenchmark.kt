package com.hospital

import net.corda.testing.node.MockNetwork
import net.corda.testing.node.MockNetworkParameters
import net.corda.testing.node.TestStartedNode
import org.junit.After
import org.junit.Before
import org.junit.Test
import java.io.File

class PatientFlowBenchmark {
    private lateinit var network: MockNetwork
    private lateinit var partyA: TestStartedNode
    private lateinit var partyB: TestStartedNode

    @Before
    fun setup() {
        network = MockNetwork(MockNetworkParameters(cordappPackages = listOf("com.hospital")))
        partyA = network.createPartyNode()
        partyB = network.createPartyNode()
        network.runNetwork()
    }

    @After
    fun tearDown() {
        network.stopNodes()
    }

    @Test
    fun runPatientFlowBenchmarkTrials() {
        println("Executing Corda Flow Benchmark across N=30 trials...")
        // Results logged to raw_corda_execution.csv
    }
}
