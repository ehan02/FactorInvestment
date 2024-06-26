# Factor-Based Investment Analysis

## Project Overview

This project is designed to implement factor-based investment strategies using Python.  It utilizes object-oriented programming principles to provide a modular, reusable, and scalable solution for loading, cleaning, and analyzing financial data. The package includes specific modules for loading data from various sources, cleaning and processing this data, and constructing investment portfolios based on factor scores.

## Components

Data Loader: A Singleton-based data loader module designed to manage and validate data from diverse sources such as CSV files and APIs.

Data Cleaner: Provides a suite of flexible strategies to preprocess financial datasets by handling missing data and winsorizing data for robust factor analysis in systematic investment.

Factor Calculator: A framework for calculating and scoring financial ratios such as PE, PB, and EV/EBITDA, utilizing abstract base classes to allow easy extension and customization for different financial metrics.

Investment Strategy: A list of various investment strategies that leverage financial factors to guide portfolio allocation decisions.

Portfolio Constructor: Tools to construct and optimize portfolios based on investment strategy to user-defined constraints

Portfolio Balancer:  Dynamically adjusts investment allocations to maintain target portfolio weights, allowing for both daily and monthly rebalancing as specified by the user.

## Contact

Echo Han - echoechohan@gmail.com

Project Link: https://github.com/ehan02/FactorInvestment/

## Acknowledgments

Alpha Vantage API for financial data

Yahoo Finance for market data