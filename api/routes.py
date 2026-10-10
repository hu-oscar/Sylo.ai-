from fastapi import APIRouter, HTTPException

router = APIRouter()


def not_implemented() -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/payments")
async def create_payment():
    not_implemented()


@router.post("/payments/{payment_id}/approve")
async def approve_payment(payment_id: str):
    not_implemented()


@router.get("/payments/{payment_id}")
async def get_payment(payment_id: str):
    not_implemented()


@router.get("/payments/{payment_id}/proof")
async def get_payment_proof(payment_id: str):
    not_implemented()


@router.post("/payees/{payee_id}/verify")
async def verify_payee(payee_id: str):
    not_implemented()


@router.get("/cases")
async def list_cases():
    not_implemented()


@router.post("/cases")
async def create_case():
    not_implemented()


@router.post("/cases/{case_id}/actions")
async def act_on_case(case_id: str):
    not_implemented()


@router.post("/sim/scene/{scene}")
async def start_scene(scene: int):
    not_implemented()


@router.post("/sim/attack/{attack}")
async def simulate_attack(attack: str):
    not_implemented()


@router.post("/sim/reset")
async def reset_simulation():
    not_implemented()


@router.get("/metrics")
async def metrics():
    not_implemented()
