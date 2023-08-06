# -*- coding: utf-8 -*-
"""
Created on Mon May  7 14:26:31 2018

@author: christoph
"""

from enum import Enum


class AccountSide(Enum):
    """ Side which the balance of an account falls on """
    DEBIT = 1
    CREDIT = -1
    BALANCED = 0

    def __repr__(self):
        return self.name


class Account:
    """ An account has two lists of debit and credit bookings """

    def __init__(self):
        self.debit = 0
        self.credit = 0

    def get_balance(self):
        debitsum = self.debit
        creditsum = self.credit
        if debitsum > creditsum:
            return (AccountSide.DEBIT, debitsum - creditsum)
        elif debitsum == creditsum:
            return(AccountSide.BALANCED, 0)
        else:
            return (AccountSide.CREDIT, creditsum - debitsum)

    def __setattr__(self, name, value):
        if name == 'debit' and hasattr(self, 'debit'):
            assert value >= self.debit
        if name == 'credit' and hasattr(self, 'credit'):
            assert value >= self.credit

        return super().__setattr__(name, value)

    def print_balance(self):
        print('debit', self.debit)
        print('credit', self.credit)


class AccountWithHistory(Account):
    """Account with additional logging of debit/credit history"""

    def __init__(self):
        super().__init__()
        self.debit_history = []
        self.credit_history = []

    def __setattr__(self, name, value):
        if name == 'debit' and hasattr(self, 'debit'):
            assert value >= self.debit
            self.debit_history.append(value)
        if name == 'credit' and hasattr(self, 'credit'):
            assert value >= self.credit
            self.credit_history.append(value)
        return super().__setattr__(name, value)