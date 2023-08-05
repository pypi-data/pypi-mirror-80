import os
import numpy as np
import pandas as pd


class CreateCases:
    """ A class of methods to create user-defined data cases
    """
    def __unit__(self):
        """ Sets the parameters and sets for the datacase
        """
        # Sets (placeholders for setting values)
        self.year = None
        self.region = None
        self.emission = None
        self.technology = None
        self.capacity_technology = None
        self.availability_technology = None
        self.fuel = None
        self.specified_fuel = None
        self.accumulated_fuel = None
        self.timeslice = None
        self.mode_of_operation = None
        self.storage = None
        self.daytype = None
        self.season = None
        self.dailytimebracket = None

        # Parameters
        self.Conversionls = None
        self.Conversionld = None
        self.Conversionlh = None
        self.DaysInDayType = None
        self.TradeRoute = None
        self.DepreciationMethod = None
        self.SpecifiedAnnualDemand = None
        self.SpecifiedDemandProfile = None
        self.AccumulatedAnnualDemand = None
        self.CapacityToActivityUnit = None
        self.CapacityFactor = None
        self.AvailabilityFactor = None
        self.OperationalLife = None
        self.ResidualCapacity = None
        self.InputActivityRatio = None
        self.OutputActivityRatio = None
        self.CapitalCost = None
        self.VariableCost = None
        self.FixedCost = None
        self.TechnologyToStorage = None
        self.TechnologyFromStorage = None
        self.StorageLevelStart = None
        self.StorageMaxChargeRate = None
        self.StorageMaxDischargeRate = None
        self.MinStorageCharge = None
        self.OperationalLifeStorage = None
        self.CapitalCostStorage = None
        self.ResidualStorageCapacity = None
        self.CapacityOfOneTechnologyUnit = None
        self.TotalAnnualMaxCapacity = None
        self.TotalAnnualMinCapacity = None
        self.TotalAnnualMaxCapacityInvestment = None
        self.TotalAnnualMinCapacityInvestment = None
        self.TotalTechnologyAnnualActivityLowerLimit = None
        self.TotalTechnologyAnnualActivityUpperLimit = None
        self.TotalTechnologyModelPeriodActivityUpperLimit = None
        self.TotalTechnologyModelPeriodActivityLowerLimit = None
        self.ReserveMarginTagTechnology = None
        self.ReserveMarginTagFuel = None
        self.ReserveMargin = None
        self.RETagTechnology = None
        self.RETagFuel = None
        self.REMinProductionTarget = None
        self.EmissionActivityRatio = None
        self.EmissionsPenalty = None
        self.AnnualExogenousEmission = None
        self.AnnualEmissionLimit = None
        self.ModelPeriodExogenousEmission = None
        self.ModelPeriodEmissionLimit = None

    def set_year(self, start_year, end_year, interval):
        """ Sets a list of forecast years

        Args:
            start_year (int): Starting year for forecasting (Less than end_year)
            end_year (int): Ending year for forecasting (Greater than start_year)
            interval (int): Gap for forecasting period
        """
        # Sets year array for new value
        year = []
        count = start_year
        while count <= end_year:
            year.append(str(count))
            count = count + interval
        self.year = year

    def set_region(self, regions):
        """ Sets the datacase's regions analysis

        Args:
            regions (list): list of regions 
        """
        self.region = regions

    def set_emission(self, emissions):
        """Sets the cases emission types

        Args:
            emissions (List): list of emission types
        """
        self.emission = emissions

    def set_technology(self, technology):
        """ Sets the cases technology type

        Args:
            technology (list): List of technologies
        """
        self.technology = technology

    def set_capacity_technology(self, capacity_technology):
        """ Sets the cases capacity_technology type

        Args:
            capacity_technology (list): List of technologies
        """
        self.capacity_technology = capacity_technology

    def set_availability_technology(self, availability_technology):
        """ Sets the cases availability_technology type

        Args:
            availability_technology (list): List of technologies
        """
        self.availability_technology = availability_technology

    def set_fuel(self, fuel):
        """ Sets the case's fuel types

        Args:
            fuel (list): list of fuels
        """
        self.fuel = fuel

    def set_specified_fuel(self, specified_fuel):
        """ Sets the case's specified fuel types

        Args:
            specified_fuel (list): list of specified fuels
        """
        self.specified_fuel = specified_fuel

    def set_accumulated_fuel(self, accumulated_fuel):
        """ Sets the case's accumulated fuel types

        Args:
            specified_fuel (list): list of specified fuels
        """
        self.accumulated_fuel = accumulated_fuel

    def set_timeslice(self, timeslice):
        """ Set of timeslices

        Args:
            timeslice (list): list of timeslices
        """
        self.timeslice = timeslice

    def set_mode_of_operation(self, num_modes_of_operation):
        """ Create the number of modes of operation (n = 1,...,num_modes_of_operation)

        Args:
            num_modes_of_operation (int): 
        """
        # Create set of mode_of_operation
        mode_of_operation = []
        count = 1
        while count <= num_modes_of_operation:
            mode_of_operation.append(str(count))
            count = count + 1
        self.mode_of_operation = mode_of_operation

    def set_storage(self, storage):
        """ Sets storage set of the datacase

        Args:
            storage (list): list of storage types
        """
        self.storage = storage

    def set_daytype(self, num_daytypes):
        """[summary]

        Args:
            num_daytypes (int): Number of daytypes
        """
        # Create set of daytypes
        daytype = []
        count = 1
        while count <= num_daytypes:
            daytype.append(str(count))
            count = count + 1
        self.daytype = daytype

    def set_season(self, num_seasons):
        """ Creates set of seasons

        Args:
            num_seasons (int): Number of seasons
        """
        # Create set of seasons
        season = []
        count = 1
        while count <= num_seasons:
            season.append(str(count))
            count = count + 1
        self.season = season

    def set_daily_time_bracket(self, num_dailytimebrackets):
        """ Creates set of daily time brackets

        Args:
            dailytimebracket (int): [description]
        """
        # Create set of dailytimebrackets
        dailytimebracket = []
        count = 1
        while count <= num_dailytimebrackets:
            dailytimebracket.append(str(count))
            count = count + 1
        self.dailytimebracket = dailytimebracket

    # Functions to define the parameters moving forward.
    def set_year_split(self, timeslices, years, splits):
        """ Creates 2D Numpy Array Parameter Splits.
            (Note: The index positions of timelices and splits must match)

        Args:
            timeslices (list): List of timeslices
            years (list): List of years
            splits (dict): A dictionary linking yearsplits to timeslices
        """
        # Creates a 2D YearSplit parameter
        YearSplit = np.ones((len(timeslices), len(years)))
        index = 0
        for time in timeslices:
            YearSplit[index, :] = splits[time]
            index = index + 1
        self.YearSplit = YearSplit

    def set_discount_rate(self, equity, debt, market_index,
                          cost_of_debt_pre_tax, risk_free_rate,
                          effective_tax_rate, preference_equity,
                          market_value_preference_shares, preference_dividends,
                          market_risk_coefficient):
        """[summary]

        Args:
            equity (dict): Dictionary of equity totals from treasury balance sheets
            debt (dict): Dictionary of equity totals from treasury balance sheets
            market_index (int, array): Regional monthly index returns (Arrays)
            cost_of_debt_pre_tax (dict): Dictionary of pre-tax cost of debts calculated from treasury balance sheets
            risk_free_rate (dict): Dictionary of risk free rates from 10 year swap rates for each region
            effective_tax_rate (dict): Dictionary of company tax rates for each region
            preference_equity (dict): Dictionary of preference equity for each region
            market_value_preference_shares (dict): Dictionary of the market value of prefence shares for each region
            preference_dividends (dict): Dictionary of prefence dividends for each region
            market_risk_coefficient (dict): Dictionary of markey risk co-efficients

        Returns:
            [int, array]: Numpy array of discount rates
        """
        # Creates empty dictionaries to stored values
        annualised_returns = {}
        cost_of_equity = {}
        cost_of_debt = {}
        cost_of_preference_equity = {}
        WACC = {}
        discount_rates = []
        # Calculates
        for region in market_index:
            # Calculates annualised returns for each regions market index
            annualised_rate_of_return = (np.power(
                (1 + ((market_index[region][-1] - market_index[region][0]) /
                      market_index[region][0])),
                (12 / len(market_index[region]))) - 1)
            annualised_returns[region] = annualised_rate_of_return
            # Calculates cost of equity
            cost_of_equity[region] = (
                risk_free_rate[region] + (market_risk_coefficient[region]) *
                (annualised_returns[region] - risk_free_rate[region]))
            # Calculates cost of debt
            cost_of_debt[region] = (cost_of_debt_pre_tax[region] / debt[region]
                                    ) * (1 - effective_tax_rate[region])
            # Calculates cost of preference equity
            cost_of_preference_equity[region] = preference_dividends[
                region] / market_value_preference_shares[region]
            # Calculates WACC
            WACC[region] = (
                cost_of_equity[region] *
                (equity[region] /
                 (equity[region] + debt[region] + preference_equity[region])) +
                cost_of_debt[region] *
                (debt[region] /
                 (equity[region] + debt[region] + preference_equity[region])) +
                cost_of_preference_equity[region] *
                (preference_equity[region] /
                 (equity[region] + debt[region] + preference_equity[region])))
            # Sets discount rates for each region
            discount_rates.append(WACC[region])
        # Set discount array
        self.DiscountRate = np.asarray(discount_rates)

    def set_day_split(self, daily_time_bracket, years, hour_split, num_days,
                      num_hours):
        """ Sets the day split parameter

        Args:
            daily_time_bracket (list): List of daily time brackets
            years (list): List of year
            hour_split (dict): Dictonary of hours in a daily time bracket 
            num_days (int): Number of days in a year
            num_hours (int): Number of hours in a day
        """
        # Initilises the DaySplit Array
        DaySplit = np.ones((len(daily_time_bracket), len(years)))
        index = 0
        for split in daily_time_bracket:
            DaySplit[index, :] = hour_split[split] / (num_days * num_hours)
            index = index + 1
        self.DaySplit = DaySplit

    def set_conversion_ls(self, timeslice, season, link):
        """ Sets the Conversionls parameter

        Args:
            timeslice (list): List of timeslices
            season (list): List of seasons
            link (dict): Dictionary describing the connection between timeslices and seasons
        """
        Conversionls = np.zeros((len(timeslice), len(season)))
        for i in range(0, len(timeslice), 1):
            for j in range(0, len(season), 1):
                if link[timeslice[i]] == season[j]:
                    Conversionls[i, j] = 1

        self.Conversionls = Conversionls

    def set_conversion_ld(self, timeslice, daytype, link):
        """ Sets the Conversionld parameter

        Args:
            timeslice (list): List of timeslices
            daytype (list): List of daytypes
            link (dict): Dictionary describing the connection between timeslices and daytypes
        """
        Conversionld = np.zeros((len(timeslice), len(daytype)))
        for i in range(0, len(timeslice), 1):
            Conversionld[i, :] = link[timeslice[i]]

        self.Conversionld = Conversionld

    def set_conversion_lh(self, timeslice, dailytimebracket, link, override):
        """ Sets the Conversionlh parameter

        Args:
            timeslice (list): List of timeslices
            dailytimebracket (list): List of dailytimebracket
            link (dict): Dictionary describing the connection between timeslices and dailytimebrackets
            override (int, array): Override if want to manually put in the array
        """
        if override == None:
            Conversionlh = np.zeros((len(timeslice), len(dailytimebracket)))
            for i in range(0, len(timeslice), 1):
                Conversionlh[i, :] = link[timeslice[i]]
            self.Conversionlh = Conversionlh
        else:
            self.Conversionlh = override

    def set_days_in_day_type(self, season, daytype, year, link, override):
        """ Sets the DaysInDayType parameter

        Args:
            season (list): List of seasons
            daytype (list): List of daytypes
            year (list): List of years
            link (dict): Dictionary relating seasons to daytypes
            override (int, array): Override if want to manually put in the array
        """
        if override == None:
            DaysInDayType = np.zeros((len(season), len(daytype), len(year)))
            for i in range(0, len(season), 1):
                for j in range(0, len(year), 1):
                    DaysInDayType[i, :, j] = link[season[i]]
            self.DaysInDayType = DaysInDayType
        else:
            self.DaysInDayType = override

    def set_trade_route(self, trade):
        """ Sets the TradeRoute parameter between regions
            (Assume it is the same across fuels and years)

        Args:
            trade (int ,array): 4D array representing trade relationships 
                                between regions, fuels and years. You 
                                must model this manually.
        """
        self.TradeRoute = trade

    def set_depreciation_method(self, region, methods, override):
        """ Sets DepreciationMethod
            (1 = Sinking Fund Depreciation, 2 = Straightline Depreciation)

        Args:
            region (list): List of regions
            override (int, array): Manual array for setting depreciation methods
            methods (dict): Dictionary assigning methods to regions
        """

        if override == None:
            depreciation_method = np.ones((len(region)))
            for i in range(0, len(region), 1):
                depreciation_method[i] = methods[region[i]]
            self.DepreciationMethod = depreciation_method
        else:
            self.DepreciationMethod = override

    def set_specified_annual_demand(self, specified_forecast):
        """ Sets the annual demand for fuels per region over the forecast period (Must be accurate)

        Args:
            forecast (float, array): The forecast array of size (len(region),len(fuel),len(year))
        """
        self.SpecifiedAnnualDemand = specified_forecast

    def set_specified_demand_profile(self, specified_annual_demand, region,
                                     fuel, year, timeslice, profile, override):
        """ Sets the specified annual demand profiles using the specified annual demand.

        Args:
            specified_annual_demand (float, array): Specified annual demand profiles
            region (list): List of regions
            fuel (list): List of fuels
            year (list): List of years
            timeslice (list): List of timeslices
            profile (Dict): Dictionary of fuel allocations to timeslices
            override (float, array): Manual override for the specified annual demand profiles.
        """
        # Initialises the linear array
        demand_profile = np.zeros(
            (len(region), len(fuel), len(timeslice), len(year)))
        if override == None:
            # Calculates the demand profile
            for place in region:
                for fuel_type in fuel:
                    for time in timeslice:
                        for year_num in year:
                            region_index = region.index(place)
                            fuel_index = fuel.index(fuel_type)
                            timeslice_index = timeslice.index(time)
                            year_index = year.index(year_num)
                            demand_profile[region_index, fuel_index,
                                           timeslice_index,
                                           year_index] = profile[time]

            self.SpecifiedDemandProfile = demand_profile
        else:
            self.SpecifiedDemandProfile = override

    def set_accumulated_annual_demand(self, accumulated_forecast):
        """ Sets the accumulated annual demand for fuels per region over the forecast period.
            This function relies on a similar forecasting methodology as set_specific_demand.
            Fuels set in this function cannot be defined in set_specific_demand.

        Args:
            accumulated_forecast (float, array): The forecast array of size (len(region),len(fuel),len(year))
        """
        self.AccumulatedAnnualDemand = accumulated_forecast

    def set_capacity_to_activity_unit(self, region, technology,
                                      capacity_dictionaries, override):
        """ Sets the capacity to activity parameter

        Args:
            region (list): List of regions
            technology (list): List of technologies
            capacity_dictionaries (list): List of dictionaries to assign value
            override (float, array) = 2D Array to assign override values
        """
        if override == None:
            cap_to_act = np.zeros((len(region), len(technology)))
            for i in range(0, len(capacity_dictionaries), 1):
                for j in range(0, len(technology), 1):
                    cap_to_act[i, j] = capacity_dictionaries[i][technology[j]]
            self.CapacityToActivityUnit = cap_to_act
        else:
            self.CapacityToActivityUnit = override

    def set_capacity_factor(self, factor_matrix):
        """ Sets capacity factors for conversion technologies.

        Args:
            factor_matrix (float, array); Capacity Factors
        """
        self.CapacityFactor = factor_matrix

    def set_availability_factor(self, availablility_matrix):
        """ Sets the availability factors

        Args:
            availablility_matrix (float, array): Matrix describing availability factors for given technologies
        """
        self.AvailabilityFactor = availablility_matrix

    def set_operational_life(self, operational_lives):
        """ Sets operational life

        Args:
            operational_lives (list):
        """
        self.OperationalLife = operational_lives

    def set_residual_capacity(self, residential_capacities):
        """ Set residual capacity

        Args:
            residential_capacities (float, array): residual capacities parameter
        """
        self.ResidualCapacity = residential_capacities

    def set_input_activity_ratio(self, input_activity_ratios):
        """ Sets input activity ratios

        Args:
            input_activity_ratios (float, array): Sets the input activity ratio
        """
        self.InputActivityRatio = input_activity_ratios

    def set_output_activity_ratio(self, output_activity_ratios):
        """ Sets output activity ratio

        Args:
            output_activity_ratios (float, array): output activity ratio parameters
        """

    def set_capital_cost(self, capital_costs):
        """ Sets capital costs

        Args:
            capital_costs (float, array): capital cost paramters
        """
        self.CapitalCost = capital_costs

    def set_variable_cost(self, variable_costs):
        """ Sets variable costs

        Args:
            variable_costs (float, array): variable costs parameters
        """
        self.VariableCost = variable_costs

    def set_fixed_cost(self, fixed_costs):
        """ Set fixed costs

        Args:
            fixed_costs (float, array): fixed cost parameters
        """
        self.FixedCost = fixed_costs

    def set_technology_to_storage(self, technology_to_storage):
        """ Sets the technology to storage parameter

        Args:
            technology_to_storage (float, array): technology to storage parameter
        """
        self.TechnologyToStorage = technology_to_storage

    def set_technology_from_storage(self, technology_from_storage):
        """ Sets technology from storage binary paramter

        Args:
            technology_from_storage (float, array): technology from storage parameter
        """
        self.TechnologyFromStorage = technology_from_storage

    def set_min_storage_charge(self, minimum_storage_charges):
        """ Sets the minimum storage charges

        Args:
            minimum_storage_charges (float, array): minimum storage parameters
        """
        self.MinStorageCharge = minimum_storage_charges

    def set_operational_life_storage(self, operational_life_storage):
        """ Sets the operational life storage

        Args:
            operational_life_storage (float, array): operational life storage parameters
        """
        self.OperationalLifeStorage = operational_life_storage

    def set_capital_cost_storage(self, capital_cost_storage):
        """ Sets the capital costs of using storage technologies

        Args:
            capital_cost_storage (float, array): capital cost of storage technologies
        """
        self.CapitalCostStorage = capital_cost_storage

    def set_storage_level_start(self, storage_level_start):
        """ Sets the storage level starting point

        Args:
            storage_level_start (float, array): storage starting level
        """
        self.StorageLevelStart = storage_level_start

    def set_storage_max_charge_rate(self, storage_max_level_charge_rates):
        """ Sets the storgae max charge rate

        Args:
            storage_max_level_charge_rates (float, array): Storage max level charge rates
        """
        self.StorageMaxChargeRate = storage_max_level_charge_rates

    def set_storage_max_discharge_rate(self,
                                       storage_max_level_discharge_rates):
        """ Sets storage technologies maximum discharge rates

        Args:
            storage_max_level_discharge_rates (float, array): Discharge rates for storage paramters
        """
        self.StorageMaxDischargeRate = storage_max_level_discharge_rates

    def set_residual_storage_capacity(self, residual_storage_capacities):
        """ Sets residual storage capacities

        Args:
            residual_storage_capacities (float, array): residual storage capacities
        """
        self.ResidualStorageCapacity = residual_storage_capacities

    def set_capacity_of_one_technology_unit(self,
                                            capacity_of_one_technology_unit):
        """ Set the capacity of one technology units for all technologies

        Args:
            capacity_of_one_technology_unit (float, array): capacities for one technology units
        """
        self.CapacityOfOneTechnologyUnit = capacity_of_one_technology_unit

    def set_total_annual_max_capacity(self, total_annual_max_capacities):
        """ Sets the total annual maximum capacities

        Args:
            total_annual_max_capacities (float, array): Total Annual Max Capacities
        """
        self.TotalAnnualMaxCapacity = total_annual_max_capacities

    def set_total_annual_min_capacity(self, total_annual_min_capacities):
        """ Sets the totoal annual minimum capacities

        Args:
            total_annual_min_capacities (float, array): Total Annual Min Capacities
        """
        self.TotalAnnualMinCapacity = total_annual_min_capacities

    def set_total_technology_annual_activity_lower_limit(
            self, total_technology_activity_lower_limits):
        """ Sets the Total Technology Activity Lower Limits

        Args:
            total_technology_activity_lower_limits (float, array): Technology Activity Lower Limits
        """
        self.TotalTechnologyAnnualActivityLowerLimit = total_technology_activity_lower_limits

    def set_total_technology_annual_activity_upper_limit(
            self, total_technology_annual_activity_upper_limits):
        """ Sets the Total Technology Activity Upper Limits

        Args:
            total_technology_annual_activity_upper_limits (float, array): Technology Activity Upper Limits
        """
        self.TotalTechnologyAnnualActivityUpperLimit = total_technology_annual_activity_upper_limits

    def set_total_technology_period_activity_upper_limit(
            self, total_technology_period_activity_upper_limits):
        """ Sets Total Technology Period Activity Upper Limits

        Args:
            total_technology_period_activity_upper_limits (float, array): Total Technology Period Activity Upper Limit
        """
        self.TotalTechnologyModelPeriodActivityUpperLimit = total_technology_period_activity_upper_limits

    def set_total_technology_period_activity_lower_limit(
            self, total_technology_period_activity_lower_limits):
        """Sets Total Technology Period Activity Lower Limits

        Args:
            total_technology_period_activity_lower_limits ([type]): Total Technology Period Activity Lower Limit
        """
        self.TotalTechnologyModelPeriodActivityLowerLimit = total_technology_period_activity_lower_limits

    def set_reserve_margin_tag_technology(self,
                                          reserve_margin_tag_technologies):
        """ Sets Reserve Margin Tag Technology

        Args:
            reserve_margin_tag_technologies (float, array): Reserve Margin Tag Technologies
        """
        self.ReserveMarginTagTechnology = reserve_margin_tag_technologies

    def set_reserve_margin_tag_fuel(self, reserve_margin_fuel_tags):
        """ Sets the reserve margin tag fuels

        Args:
            reserve_margin_fuel_tags (float, array): Sets the reserve margin tag fuel parameters
        """
        self.ReserveMarginTagFuel = reserve_margin_fuel_tags

    def set_reserve_margin(self, reserve_margins):
        """ Sets reserve margins

        Args:
            reserve_margins (float, array): Reserve Margins
        """
        self.ReserveMargin = reserve_margins

    def set_re_tag_technology(self, re_tag_technologies):
        """ Sets RE Tag Technology

        Args:
            re_tag_technologies (float, array): RE Tag Technologies
        """
        self.RETagTechnology = re_tag_technologies

    def set_re_tag_fuel(self, re_tag_fuels):
        """ Sets RE Tag Fuels

        Args:
            re_tag_fuels (float, array): RE Tag Fuels
        """
        self.RETagFuel = re_tag_fuels

    def set_re_min_production_target(self, re_min_production_targets):
        """ Sets Renewable Energy Minimum Production Targets

        Args:
            re_min_production_targets (float, array): Renewable Energy Minimum Production Targets
        """
        self.REMinProductionTarget = re_min_production_targets

    def set_emission_activity_ratio(self, emission_activity_ratios):
        """ Sets Emission Activity Ratios

        Args:
            emission_activity_ratios ([float, array): Emission Activity Ratios
        """
        self.EmissionActivityRatio = emission_activity_ratios

    def set_emissions_penalty(self, emissions_penalties):
        """ Sets Emissions Penalties

        Args:
            emissions_penalties (float, penalties): Emissions Penalties
        """
        self.EmissionsPenalty = emissions_penalties

    def set_annual_exogenous_emission(self, annual_exogenous_emission):
        """ Sets Annual Exogneous Emissions

        Args:
            annual_exogenous_emission (float, array): Annual Exogenous Emissions
        """
        self.AnnualExogenousEmission = annual_exogenous_emission

    def set_annual_emission_limit(self, annual_emission_limits):
        """ Sets Annual Emission Limits

        Args:
            annual_emission_limits (float, array): Annual Emission Limits
        """
        self.AnnualEmissionLimit = annual_emission_limits

    def set_model_period_exogenous_emission(self,
                                            model_period_exogenous_emissions):
        """ Sets Model Period Exogenous Emissions

        Args:
            model_period_exogenous_emissions (float, array): Model Period Exogenous Emissions
        """
        self.ModelPeriodExogenousEmission = model_period_exogenous_emissions

    def set_model_period_emission_limit(self, model_period_emission_limits):
        """ Sets Model Period Emission Limits

        Args:
            model_period_emission_limits (float, array): Model Period Emission Limits
        """
        self.ModelPeriodEmissionLimit = model_period_emission_limits