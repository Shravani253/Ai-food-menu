// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract FoodTraceabilityIndustry {

    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not contract owner");
        _;
    }

    // ------------------ ENUMS ------------------

    enum Actor { Farmer, Manufacturer, Transporter, Retailer, AI }
    enum BatchStatus { Created, InTransit, ForSale, Sold, Recalled }

    // ------------------ STRUCTS ------------------

    struct ActorProfile {
        Actor role;
        bool active;
        string licenseId;
    }

    struct AIProof {
        bytes32 modelHash;
        uint confidence;
    }

    struct TraceRecord {
        bytes32 action;
        Actor actor;
        uint timestamp;
        AIProof aiProof;
    }

    struct Batch {
        string foodName;
        BatchStatus status;
        bool recalled;
    }

    // ------------------ STORAGE ------------------

    mapping(address => ActorProfile) public actors;
    mapping(bytes32 => Batch) public batches;
    mapping(bytes32 => TraceRecord[]) private batchHistory;

    // ------------------ EVENTS ------------------

    event ActorRegistered(address actor, Actor role);
    event BatchCreated(bytes32 batchId, string foodName);
    event RecordAdded(bytes32 batchId, bytes32 action, Actor actor);
    event BatchRecalled(bytes32 batchId, string reason);

    // ------------------ MODIFIERS ------------------

    modifier onlyActiveActor(Actor _role) {
        require(actors[msg.sender].active, "Actor not active");
        require(actors[msg.sender].role == _role, "Invalid role");
        _;
    }

    // ------------------ ACTOR MANAGEMENT ------------------

    function registerActor(
        address _actor,
        Actor _role,
        string memory _licenseId
    ) public onlyOwner {
        actors[_actor] = ActorProfile(_role, true, _licenseId);
        emit ActorRegistered(_actor, _role);
    }

    // ------------------ BATCH MANAGEMENT ------------------

    function createBatch(bytes32 _batchId, string memory _foodName)
        public
        onlyActiveActor(Actor.Farmer)
    {
        batches[_batchId] = Batch(_foodName, BatchStatus.Created, false);
        emit BatchCreated(_batchId, _foodName);
    }

    // ------------------ TRACEABILITY ------------------

    function addTraceRecord(
        bytes32 _batchId,
        bytes32 _action,
        bytes32 _modelHash,
        uint _confidence
    ) public {

        require(!batches[_batchId].recalled, "Batch recalled");

        TraceRecord memory record = TraceRecord({
            action: _action,
            actor: actors[msg.sender].role,
            timestamp: block.timestamp,
            aiProof: AIProof(_modelHash, _confidence)
        });

        batchHistory[_batchId].push(record);
        emit RecordAdded(_batchId, _action, actors[msg.sender].role);
    }

    // ------------------ RECALL ------------------

    function recallBatch(bytes32 _batchId, string memory _reason)
        public
        onlyOwner
    {
        batches[_batchId].recalled = true;
        batches[_batchId].status = BatchStatus.Recalled;
        emit BatchRecalled(_batchId, _reason);
    }

    // ------------------ READ FUNCTIONS ------------------

    function getHistoryCount(bytes32 _batchId)
        public
        view
        returns (uint)
    {
        return batchHistory[_batchId].length;
    }

    function getRecord(bytes32 _batchId, uint index)
        public
        view
        returns (
            bytes32,
            Actor,
            uint,
            bytes32,
            uint
        )
    {
        TraceRecord memory r = batchHistory[_batchId][index];
        return (
            r.action,
            r.actor,
            r.timestamp,
            r.aiProof.modelHash,
            r.aiProof.confidence
        );
    }
}
