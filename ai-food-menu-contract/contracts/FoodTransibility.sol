// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract FoodTraceability {

    // Roles involved in supply chain
    enum Actor {
        Farmer,
        Manufacturer,
        Transporter,
        Retailer,
        AI
    }

    // Structure to store each trace record
    struct TraceRecord {
        string batchId;
        string foodName;
        string action;          // e.g. Harvested, Processed, Transported, AI Analyzed
        string aiResult;        // Fresh / Stale / Quality Grade
        uint confidence;        // AI confidence %
        Actor actor;
        uint timestamp;
    }

    // Mapping batchId => list of records
    mapping(string => TraceRecord[]) private foodHistory;

    // Event for frontend notification
    event RecordAdded(
        string batchId,
        string action,
        Actor actor,
        uint timestamp
    );

    // Add new record (called by backend / AI)
    function addRecord(
        string memory _batchId,
        string memory _foodName,
        string memory _action,
        string memory _aiResult,
        uint _confidence,
        Actor _actor
    ) public {

        TraceRecord memory record = TraceRecord({
            batchId: _batchId,
            foodName: _foodName,
            action: _action,
            aiResult: _aiResult,
            confidence: _confidence,
            actor: _actor,
            timestamp: block.timestamp
        });

        foodHistory[_batchId].push(record);

        emit RecordAdded(_batchId, _action, _actor, block.timestamp);
    }

    // Get total records for a batch
    function getRecordCount(string memory _batchId)
        public
        view
        returns (uint)
    {
        return foodHistory[_batchId].length;
    }

    // Get specific record by index
    function getRecordByIndex(
        string memory _batchId,
        uint index
    )
        public
        view
        returns (
            string memory,
            string memory,
            string memory,
            string memory,
            uint,
            Actor,
            uint
        )
    {
        TraceRecord memory record = foodHistory[_batchId][index];

        return (
            record.batchId,
            record.foodName,
            record.action,
            record.aiResult,
            record.confidence,
            record.actor,
            record.timestamp
        );
    }
}
