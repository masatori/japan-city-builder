"""Detailed taxation and law system."""

import logging
from typing import Dict, List, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class TaxBracket:
    """Represents a tax bracket for progressive taxation."""
    
    def __init__(self, income_threshold: float, tax_rate: float):
        """Initialize tax bracket.
        
        Args:
            income_threshold: Income level at which this bracket starts
            tax_rate: Tax rate for this bracket (0.0-1.0)
        """
        self.income_threshold = income_threshold
        self.tax_rate = tax_rate
    
    def calculate_tax(self, income: float) -> float:
        """Calculate tax for given income.
        
        Args:
            income: Income amount
        
        Returns:
            Tax amount
        """
        if income < self.income_threshold:
            return 0
        return (income - self.income_threshold) * self.tax_rate


class TaxSystem:
    """Manages all taxation for the city."""
    
    def __init__(self):
        """Initialize tax system with default rates."""
        # Citizen income tax brackets (progressive)
        self.citizen_tax_brackets = [
            TaxBracket(0, 0.00),           # No tax below minimum
            TaxBracket(20000, 0.05),       # 5% above 20k
            TaxBracket(50000, 0.10),       # 10% above 50k
            TaxBracket(100000, 0.15),      # 15% above 100k
            TaxBracket(200000, 0.20),      # 20% above 200k
        ]
        
        # Business tax rates by industry
        self.industry_tax_rates = {
            'residential': 0.08,
            'commercial': 0.12,
            'industrial': 0.10,
            'tourism': 0.15,
            'agriculture': 0.06,
        }
        
        # Property tax rate (% of property value per year)
        self.property_tax_rate = 0.015
        
        # Corporate tax rate
        self.corporate_tax_rate = 0.20
        
        # Sales tax rate
        self.sales_tax_rate = 0.08
        
        # Special taxes and fees
        self.vehicle_registration_tax = 0.03  # % of vehicle value
        self.luxury_tax_threshold = 50000  # Income threshold for luxury tax
        self.luxury_tax_rate = 0.30
        
        # Tax exemptions and incentives
        self.tax_exemptions = []  # Building IDs that are tax-exempt
        self.tax_incentives = {}  # Building ID -> incentive rate
        
        # Tax collection efficiency (0.0-1.0)
        self.collection_efficiency = 0.85
        
        # Audit rate for tax evasion
        self.audit_rate = 0.05
        self.tax_evasion_penalty = 0.30  # 30% penalty on evaded taxes
    
    def calculate_citizen_tax(self, citizen_income: float) -> float:
        """Calculate income tax for a citizen using progressive taxation.
        
        Args:
            citizen_income: Annual income
        
        Returns:
            Tax amount
        """
        total_tax = 0
        
        # Sort brackets by threshold
        sorted_brackets = sorted(self.citizen_tax_brackets, key=lambda b: b.income_threshold)
        
        # Calculate tax using marginal rate system
        for i, bracket in enumerate(sorted_brackets):
            if citizen_income > bracket.income_threshold:
                # Find next bracket threshold
                next_threshold = sorted_brackets[i + 1].income_threshold if i + 1 < len(sorted_brackets) else float('inf')
                
                # Calculate taxable income in this bracket
                taxable_in_bracket = min(citizen_income, next_threshold) - bracket.income_threshold
                total_tax += taxable_in_bracket * bracket.tax_rate
        
        return total_tax
    
    def calculate_luxury_tax(self, citizen_income: float) -> float:
        """Calculate luxury tax on high earners.
        
        Args:
            citizen_income: Annual income
        
        Returns:
            Luxury tax amount
        """
        if citizen_income > self.luxury_tax_threshold:
            excess = citizen_income - self.luxury_tax_threshold
            return excess * self.luxury_tax_rate
        return 0
    
    def calculate_business_tax(self, business_income: float, industry_type: str, 
                              is_exempted: bool = False) -> float:
        """Calculate business tax.
        
        Args:
            business_income: Annual business income
            industry_type: Type of industry
            is_exempted: Whether business is tax-exempt
        
        Returns:
            Business tax amount
        """
        if is_exempted:
            return 0
        
        rate = self.industry_tax_rates.get(industry_type, 0.10)
        base_tax = business_income * rate
        
        # Apply corporate tax on profits
        corporate_portion = base_tax * self.corporate_tax_rate
        
        return base_tax + corporate_portion
    
    def calculate_property_tax(self, property_value: float, is_exempted: bool = False) -> float:
        """Calculate annual property tax.
        
        Args:
            property_value: Assessed value of property
            is_exempted: Whether property is exempt
        
        Returns:
            Annual property tax
        """
        if is_exempted:
            return 0
        return property_value * self.property_tax_rate
    
    def calculate_sales_tax(self, transaction_value: float) -> float:
        """Calculate sales tax on transaction.
        
        Args:
            transaction_value: Transaction amount
        
        Returns:
            Sales tax amount
        """
        return transaction_value * self.sales_tax_rate
    
    def set_tax_rate(self, tax_type: str, rate: float) -> bool:
        """Set custom tax rate.
        
        Args:
            tax_type: Type of tax to adjust
            rate: New tax rate (0.0-1.0)
        
        Returns:
            True if successful
        """
        if tax_type == 'corporate':
            self.corporate_tax_rate = max(0, min(1.0, rate))
            logger.info(f"Corporate tax rate set to {self.corporate_tax_rate * 100}%")
            return True
        elif tax_type == 'sales':
            self.sales_tax_rate = max(0, min(1.0, rate))
            logger.info(f"Sales tax rate set to {self.sales_tax_rate * 100}%")
            return True
        elif tax_type == 'property':
            self.property_tax_rate = max(0, min(1.0, rate))
            logger.info(f"Property tax rate set to {self.property_tax_rate * 100}%")
            return True
        return False
    
    def set_industry_tax_rate(self, industry: str, rate: float) -> bool:
        """Set tax rate for specific industry.
        
        Args:
            industry: Industry type
            rate: Tax rate (0.0-1.0)
        
        Returns:
            True if successful
        """
        if industry in self.industry_tax_rates:
            self.industry_tax_rates[industry] = max(0, min(1.0, rate))
            logger.info(f"{industry.capitalize()} tax rate set to {rate * 100}%")
            return True
        return False
    
    def add_tax_exemption(self, building_id: str):
        """Grant tax exemption to building.
        
        Args:
            building_id: ID of building to exempt
        """
        if building_id not in self.tax_exemptions:
            self.tax_exemptions.append(building_id)
            logger.info(f"Tax exemption granted to {building_id}")
    
    def remove_tax_exemption(self, building_id: str):
        """Remove tax exemption from building.
        
        Args:
            building_id: ID of building
        """
        if building_id in self.tax_exemptions:
            self.tax_exemptions.remove(building_id)
            logger.info(f"Tax exemption removed from {building_id}")
    
    def add_tax_incentive(self, building_id: str, incentive_rate: float):
        """Add tax incentive to building.
        
        Args:
            building_id: ID of building
            incentive_rate: Reduction in tax rate (0.0-1.0)
        """
        self.tax_incentives[building_id] = incentive_rate
        logger.info(f"Tax incentive of {incentive_rate * 100}% added to {building_id}")
    
    def get_tax_summary(self) -> Dict[str, float]:
        """Get summary of all tax rates.
        
        Returns:
            Dictionary of tax rates
        """
        return {
            'corporate_tax': self.corporate_tax_rate,
            'sales_tax': self.sales_tax_rate,
            'property_tax': self.property_tax_rate,
            'luxury_tax_rate': self.luxury_tax_rate,
            'collection_efficiency': self.collection_efficiency,
        }


class LawSystem:
    """Manages laws and regulations for the city."""
    
    def __init__(self):
        """Initialize law system."""
        # Zoning laws
        self.zoning_restrictions = {}
        
        # Building regulations (height limits, setbacks, etc.)
        self.height_limits = {'residential': 10, 'commercial': 30, 'industrial': 25}
        
        # Environmental regulations
        self.pollution_limits = {'residential': 30, 'commercial': 50, 'industrial': 70}
        self.noise_limits = {'residential': 55, 'commercial': 70, 'industrial': 85}  # dB
        
        # Labor laws
        self.minimum_wage = 1000  # Per hour
        self.maximum_work_hours = 40  # Per week
        self.child_labor_allowed = False
        
        # Building codes
        self.fire_safety_required = True
        self.earthquake_resistance_required = True
        self.accessibility_required = True
        
        # Traffic regulations
        self.speed_limits = {'residential': 30, 'commercial': 40, 'highway': 100}  # km/h
        self.parking_requirements = {'residential': 1.5, 'commercial': 2.0}  # spaces per unit
        
        # Business regulations
        self.business_licenses_required = True
        self.health_inspections_required = True
        self.environmental_impact_assessments = True
        
        logger.info("Law system initialized")
    
    def can_build(self, building_type: str, location_x: int, location_y: int, 
                  height: int) -> Tuple[bool, str]:
        """Check if building is allowed under current laws.
        
        Args:
            building_type: Type of building
            location_x, location_y: Building location
            height: Building height in stories
        
        Returns:
            Tuple of (allowed: bool, reason: str)
        """
        # Check height limit
        if building_type in self.height_limits:
            limit = self.height_limits[building_type]
            if height > limit:
                return False, f"Building exceeds height limit of {limit} stories"
        
        return True, "Building allowed"
    
    def set_pollution_limit(self, zone_type: str, limit: float):
        """Set pollution limit for zone type.
        
        Args:
            zone_type: Type of zone
            limit: Pollution limit (0-100)
        """
        self.pollution_limits[zone_type] = limit
        logger.info(f"Pollution limit for {zone_type} set to {limit}")
    
    def set_height_limit(self, building_type: str, stories: int):
        """Set maximum building height.
        
        Args:
            building_type: Type of building
            stories: Maximum stories allowed
        """
        self.height_limits[building_type] = stories
        logger.info(f"Height limit for {building_type} set to {stories} stories")
    
    def set_minimum_wage(self, wage: float):
        """Set minimum wage.
        
        Args:
            wage: Hourly wage
        """
        self.minimum_wage = wage
        logger.info(f"Minimum wage set to {wage} per hour")
    
    def get_regulations_summary(self) -> Dict:
        """Get summary of all regulations.
        
        Returns:
            Dictionary of regulations
        """
        return {
            'height_limits': self.height_limits,
            'pollution_limits': self.pollution_limits,
            'minimum_wage': self.minimum_wage,
            'speed_limits': self.speed_limits,
        }
