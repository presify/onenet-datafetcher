from pydantic import BaseModel, Field
from typing import List
from typing import Optional
#= Field(..., gt=37, le=100)

class Load(BaseModel):
  periodStart: str
  periodEnd: str
  outBiddingZone_Domain: str
  loadType: str
  securityToken: str
  documentType: str = "A65"


class Generation(BaseModel):
  periodStart: str
  periodEnd: str
  securityToken: str
  in_Domain: str
  processType: str = "A33"
  documentType: str = "A68"
  generationType: str = "Default"

class Transmission(BaseModel):
  periodStart: str
  periodEnd: str
  securityToken: str
  in_Domain: str
  out_Domain: str
  documentType: str = "Default"
  transmissionType: str = "Default"

class Balancing(BaseModel):
  periodStart: str
  periodEnd: str
  securityToken: str
  controlArea_Domain: str
  balancingType: str = "Default"

