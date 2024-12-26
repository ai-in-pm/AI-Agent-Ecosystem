from typing import Dict, Any, List
from datetime import datetime, timedelta
from core.base_agent import BaseAgent

class InfluencerOutreachAgent(BaseAgent):
    """Agent responsible for managing influencer relationships and campaigns."""
    
    async def initialize(self) -> bool:
        """Initialize influencer outreach systems."""
        self.influencer_tiers = {
            "nano": {
                "followers": (1000, 10000),
                "engagement_rate": 0.05,
                "max_budget": 500
            },
            "micro": {
                "followers": (10000, 50000),
                "engagement_rate": 0.04,
                "max_budget": 2000
            },
            "mid": {
                "followers": (50000, 500000),
                "engagement_rate": 0.03,
                "max_budget": 10000
            },
            "macro": {
                "followers": (500000, 1000000),
                "engagement_rate": 0.02,
                "max_budget": 50000
            }
        }
        
        self.active_campaigns = {}
        self.influencer_database = {}
        self.campaign_metrics = {}
        return True
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute influencer outreach tasks."""
        if task["type"] == "identify_influencers":
            return await self._identify_influencers(
                criteria=task["criteria"],
                count=task["count"]
            )
        elif task["type"] == "create_campaign":
            return await self._create_campaign(task["campaign_details"])
        elif task["type"] == "track_performance":
            return await self._track_campaign_performance(task["campaign_id"])
            
        return {"status": "error", "message": "Unknown task type"}
    
    async def monitor(self) -> Dict[str, Any]:
        """Monitor influencer campaigns and relationships."""
        campaign_status = self._check_campaign_status()
        roi_metrics = await self._calculate_roi_metrics()
        
        return {
            "active_campaigns": len(self.active_campaigns),
            "campaign_status": campaign_status,
            "roi_metrics": roi_metrics,
            "last_check": datetime.utcnow().isoformat()
        }
    
    async def _identify_influencers(
        self,
        criteria: Dict[str, Any],
        count: int
    ) -> Dict[str, Any]:
        """Identify suitable influencers based on criteria."""
        matching_influencers = []
        
        for influencer_id, data in self.influencer_database.items():
            if self._matches_criteria(data, criteria):
                matching_influencers.append({
                    "id": influencer_id,
                    "metrics": data["metrics"],
                    "fit_score": self._calculate_fit_score(data, criteria)
                })
                
        # Sort by fit score and return top matches
        matching_influencers.sort(key=lambda x: x["fit_score"], reverse=True)
        return {
            "status": "success",
            "influencers": matching_influencers[:count]
        }
    
    async def _create_campaign(
        self,
        campaign_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create and initialize new influencer campaign."""
        campaign_id = f"campaign_{datetime.utcnow().timestamp()}"
        
        # Validate budget against tier limits
        if not self._validate_campaign_budget(
            campaign_details["influencers"],
            campaign_details["budget"]
        ):
            return {"status": "error", "message": "Budget exceeds tier limits"}
            
        self.active_campaigns[campaign_id] = {
            "details": campaign_details,
            "status": "active",
            "start_date": datetime.utcnow().isoformat(),
            "metrics": {}
        }
        
        return {
            "status": "success",
            "campaign_id": campaign_id,
            "start_date": datetime.utcnow().isoformat()
        }
    
    async def _track_campaign_performance(
        self,
        campaign_id: str
    ) -> Dict[str, Any]:
        """Track performance metrics for specific campaign."""
        if campaign_id not in self.active_campaigns:
            return {"status": "error", "message": "Campaign not found"}
            
        metrics = await self._gather_campaign_metrics(campaign_id)
        roi = self._calculate_campaign_roi(campaign_id, metrics)
        
        self.campaign_metrics[campaign_id] = {
            "metrics": metrics,
            "roi": roi,
            "last_updated": datetime.utcnow().isoformat()
        }
        
        return {
            "status": "success",
            "campaign_id": campaign_id,
            "metrics": metrics,
            "roi": roi
        }
    
    def _matches_criteria(
        self,
        influencer_data: Dict[str, Any],
        criteria: Dict[str, Any]
    ) -> bool:
        """Check if influencer matches specified criteria."""
        for key, value in criteria.items():
            if key not in influencer_data:
                return False
            if isinstance(value, tuple):
                if not (value[0] <= influencer_data[key] <= value[1]):
                    return False
            elif influencer_data[key] != value:
                return False
        return True
    
    def _calculate_fit_score(
        self,
        influencer_data: Dict[str, Any],
        criteria: Dict[str, Any]
    ) -> float:
        """Calculate how well an influencer fits the criteria."""
        # Implementation would include scoring logic
        return 0.9
    
    def _validate_campaign_budget(
        self,
        influencers: List[Dict[str, Any]],
        budget: float
    ) -> bool:
        """Validate campaign budget against tier limits."""
        for influencer in influencers:
            tier = self._get_influencer_tier(influencer["metrics"]["followers"])
            if budget > self.influencer_tiers[tier]["max_budget"]:
                return False
        return True
    
    def _get_influencer_tier(self, followers: int) -> str:
        """Determine influencer tier based on follower count."""
        for tier, data in self.influencer_tiers.items():
            if data["followers"][0] <= followers <= data["followers"][1]:
                return tier
        return "macro"
    
    async def _gather_campaign_metrics(
        self,
        campaign_id: str
    ) -> Dict[str, Any]:
        """Gather performance metrics for campaign."""
        # In a real implementation, this would gather actual metrics
        return {
            "impressions": 0,
            "engagement": 0,
            "clicks": 0,
            "conversions": 0
        }
    
    def _calculate_campaign_roi(
        self,
        campaign_id: str,
        metrics: Dict[str, Any]
    ) -> float:
        """Calculate ROI for campaign."""
        campaign = self.active_campaigns[campaign_id]
        cost = campaign["details"]["budget"]
        revenue = metrics["conversions"] * campaign["details"]["conversion_value"]
        return (revenue - cost) / cost if cost > 0 else 0
    
    def _check_campaign_status(self) -> Dict[str, str]:
        """Check status of all active campaigns."""
        status = {}
        for campaign_id, campaign in self.active_campaigns.items():
            if campaign["status"] == "active":
                if self._is_performing_well(campaign_id):
                    status[campaign_id] = "healthy"
                else:
                    status[campaign_id] = "needs_attention"
            else:
                status[campaign_id] = campaign["status"]
        return status
    
    def _is_performing_well(self, campaign_id: str) -> bool:
        """Check if campaign is meeting performance targets."""
        if campaign_id not in self.campaign_metrics:
            return True
        metrics = self.campaign_metrics[campaign_id]
        return metrics["roi"] > 0.2  # 20% ROI threshold
    
    async def _calculate_roi_metrics(self) -> Dict[str, float]:
        """Calculate ROI metrics across all campaigns."""
        total_cost = 0
        total_revenue = 0
        
        for campaign_id, campaign in self.active_campaigns.items():
            if campaign_id in self.campaign_metrics:
                metrics = self.campaign_metrics[campaign_id]
                total_cost += campaign["details"]["budget"]
                total_revenue += metrics["roi"] * campaign["details"]["budget"]
                
        return {
            "total_cost": total_cost,
            "total_revenue": total_revenue,
            "overall_roi": (total_revenue - total_cost) / total_cost if total_cost > 0 else 0
        }
