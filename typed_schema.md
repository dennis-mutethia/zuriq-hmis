# Zuriq 1.0 — Typed Schema (from decompiled DataSet classes)

Each table below is a strongly-typed ADO.NET DataTable found in the decompiled source, with real .NET column types. Table/class names are the DataSet's internal name, not always identical to the MySQL table name (cross-reference with inferred_schema.md for actual `tbl...` names).

## dT301InpatientDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.MOHDatasets/_Ds301Inpatient.cs)_
- **Age**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **Residence**: `string`
- **PostalAddress**: `string`
- **CityTown**: `string`
- **InPatientNo**: `int`
- **Telephone1**: `string`
- **IsReferal**: `int`
- **ReferalReason**: `string`
- **IsAlive**: `int`
- **AdmissionDateTime**: `DateTime`
- **DischargeDateTime**: `DateTime`
- **Diagnosis**: `string`
- **DischargePrescription**: `string`
- **TreatmentGiven**: `string`
- **Comments**: `string`
- **Admittedduration**: `string`

## dTARInvFiltByGrpAccDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsARInvFiltByGroupAcc.cs)_
- **HospitalName**: `string`
- **LetterHead**: `string`
- **HospitalInfoID**: `int`
- **ARInvoiceNo**: `int`
- **DateTimeCreated**: `DateTime`
- **InvoiceTo**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **PrincipalMember**: `string`
- **MembershipNo**: `string`
- **ARInvoiceID**: `int`
- **TotalAmountPaid**: `double`
- **DueDate**: `DateTime`
- **AmountReceivable**: `double`
- **IsPaid**: `int`
- **CoverAmount**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **ReceivableAccSubAccID**: `int`
- **GroupAccountName**: `string`
- **PhysicalAddress**: `string`
- **PostalAddress**: `string`
- **PostalCode**: `string`
- **TownCity**: `string`
- **Telephone1**: `string`
- **EmailAddress**: `string`
- **CompanyName**: `string`
- **Sponsor**: `string`
- **OrderNo**: `string`

## dTARInvoiceDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsARInvoice.cs)_
- **HospitalName**: `string`
- **ARInvoiceNo**: `int`
- **DateTimeCreatedARInvoice**: `DateTime`
- **DueDate**: `DateTime`
- **AmountReceivable**: `double`
- **IsPaid**: `int`
- **InvoiceTo**: `string`
- **Address**: `string`
- **Telephone1**: `string`
- **Telephone2**: `string`
- **LetterHead**: `string`
- **Username**: `string`
- **VisitID**: `int`
- **DateTimeCreated**: `DateTime`
- **TotalBillAmount**: `double`
- **Balance**: `double`
- **MedicalBillNo**: `int`
- **BillTotalAmountPaid**: `double`
- **ARInvoiceTotalAmountPaid**: `double`
- **CustomerName**: `string`
- **CoverAmount**: `double`
- **SalesDiscountAmount**: `double`
- **TotalBillAmount1**: `float`
- **BillTotalAmountPaid1**: `float`
- **HasBeenCancelled**: `int`

## dTARInvoiceReceiptDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsARInvoiceReceipt.cs)_
- **IssuedReceiptNo**: `int`
- **DateTimeIssued**: `DateTime`
- **AmountPaid**: `double`
- **AmountReceived**: `double`
- **ChangeAmount**: `double`
- **PaidInBy**: `string`
- **IssuedTo**: `string`
- **Description**: `string`
- **LetterHead**: `string`
- **ARInvoiceNo**: `int`
- **HospitalName**: `string`
- **Username**: `string`
- **PaymentFor**: `string`
- **MedicalBillNo**: `int`
- **PaymentModeID**: `int`
- **PaymentMode**: `string`

## dTARInvoicesDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsARInvoices.cs)_
- **HospitalName**: `string`
- **LetterHead**: `string`
- **ARInvoiceNo**: `int`
- **DateTimeCreated**: `DateTime`
- **AmountReceivable**: `double`
- **InvoiceTo**: `string`
- **TotalAmountPaid**: `double`
- **MedicalBillNo**: `int`
- **CustomerName**: `string`
- **DueDate**: `DateTime`
- **IsPaid**: `int`
- **SalesDiscountAmount**: `double`
- **CoverAmount**: `double`
- **OutPatientNo**: `int`
- **Telephone1**: `string`
- **Address**: `string`
- **Telephone2**: `string`
- **EmailAddress**: `string`
- **WriteOffAmount**: `double`

## dTAdmissionFormInfoDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsAdmissionFormInfor.cs)_
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Occupation**: `string`
- **Residence**: `string`
- **NextOfKin**: `string`
- **NextOfKinRelationship**: `string`
- **NextOfKinContact**: `string`
- **GroupAccountID**: `int`
- **Name**: `string`
- **PrincipalMember**: `string`
- **MembershipNo**: `string`
- **CompanyName**: `string`
- **HospitalInfoID**: `int`
- **Expr1**: `string`
- **LetterHead**: `string`
- **AdmissionID**: `int`
- **HPI**: `string`
- **AdmissionDateTime**: `DateTime`
- **PastMedicalHistory**: `string`
- **ReviewOfSystems**: `string`
- **SocialHabits**: `string`
- **GeneralCondition**: `string`
- **Allergies**: `string`
- **Temperature**: `string`
- **Pulse**: `string`
- **RespirationRate**: `string`
- **BloodPressure**: `string`
- **Investigations**: `string`
- **Treatment**: `string`
- **Diagnosis**: `string`
- **DateTimePosted**: `DateTime`
- **IDNumber**: `string`
- **OutPatientNo**: `int`
- **Telephone1**: `string`
- **AdmittingDoctor**: `string`

## dTAdmissionNotesDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsAdmissionNotes.cs)_
- **VisitID**: `int`
- **AdmissionDateTime**: `DateTime`
- **AdmittingDoctor**: `string`
- **DateTimePosted**: `DateTime`
- **Notes**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **PostalAddress**: `string`
- **IDNumber**: `string`
- **OutPatientNo**: `int`
- **Telephone1**: `string`
- **Name**: `string`
- **Username**: `string`
- **LetterHead**: `string`
- **AdmissionID**: `int`

## dTAdmittedBillsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsInpatientBillsSum.cs)_
- **HospitalName**: `string`
- **IsInAdmission**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **BedNo**: `string`
- **AdmissionID**: `int`
- **IsCurrentBed**: `int`
- **AdmissionDateTime**: `DateTime`
- **Ward**: `string`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **CoverAmount**: `double`
- **DepositOffset**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **DepositBalance**: `double`
- **GroupAccount**: `string`

## dTAdmittedByDocSummDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatBills/_DsAdmittedPatientsByDocSumm.cs)_
- **Name**: `string`
- **LetterHead**: `string`
- **AdmissionID**: `int`
- **AdmissionDateTime**: `DateTime`
- **AdmittingDoctor**: `string`

## dTAllPatientReByAccountDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsAllPatientReByAccount.cs)_
- **VisitDateTime**: `DateTime`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **Age**: `int`
- **Diagnosis**: `string`
- **Doctor**: `string`
- **VisitID**: `int`
- **HospitalName**: `string`
- **TotalBillAmount**: `float`
- **AgeMonths**: `int`
- **AgeWeeks**: `int`
- **Name**: `string`
- **IDNumber**: `string`
- **MembershipNo**: `string`
- **LetterHead**: `string`
- **TotalAmountPaid**: `float`
- **CustomerName**: `string`
- **ClinicID**: `int`
- **Expr1**: `string`

## dTAllPatientReDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsAllPatientRe.cs)_
- **VisitDateTime**: `DateTime`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **Age**: `int`
- **Diagnosis**: `string`
- **Doctor**: `string`
- **VisitID**: `int`
- **HospitalName**: `string`
- **TotalBillAmount**: `float`
- **AgeMonths**: `int`
- **AgeWeeks**: `int`
- **Name**: `string`
- **IDNumber**: `string`
- **MembershipNo**: `string`
- **LetterHead**: `string`
- **ClinicID**: `int`
- **Expr1**: `string`

## dTAssetsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsAssetRegister.cs)_
- **AssetRegisterID**: `int`
- **Name**: `string`
- **Model**: `string`
- **Units**: `int`
- **CostPerUnit**: `double`
- **Status**: `string`
- **DepartmentID**: `int`
- **Expr1**: `string`
- **HospitalInfoID**: `int`
- **Expr2**: `string`
- **LetterHead**: `string`
- **StorageLocationID**: `int`
- **Expr3**: `string`

## dTBankAdjustmentDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsBankRec.cs)_
- **BankRecID**: `int`
- **SourceReference**: `string`
- **Description**: `string`
- **Amount**: `double`
- **StatementBalance**: `double`
- **IsBankAdjustingItem**: `int`
- **IsIncrement**: `int`
- **IsAdjustment**: `int`
- **FromDateTime**: `DateTime`
- **ToDateTime**: `DateTime`

## dTBankDepositsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsBankDeposits.cs)_
- **SubAccount**: `string`
- **TotalAmountDeposited**: `float`
- **DateTimeDeposited**: `DateTime`
- **Username**: `string`
- **DepositedBy**: `string`
- **TransactionDateTime**: `DateTime`
- **TransactedBySysUID**: `int`
- **BankTransactionRefNo**: `string`
- **JournalVoucherID**: `int`
- **ChequeNos**: `string`
- **TotalAmount**: `double`
- **AmountInWords**: `string`
- **Name**: `string`
- **LetterHead**: `string`

## dTBankRecDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsBankRec.cs)_
- **HospitalName**: `string`
- **FromDateTime**: `DateTime`
- **ToDateTime**: `DateTime`
- **HasBeenReconciled**: `int`
- **BankRecID**: `int`
- **ReconciledBy**: `string`
- **StatementBalance**: `double`
- **BookBalance**: `double`
- **SourceReference**: `string`
- **Description**: `string`
- **Amount**: `double`
- **IsBankAdjustingItem**: `int`
- **IsBookAdjustingItem**: `int`
- **IsIncrement**: `int`
- **IsAdjustment**: `int`

## dTBedOccupancyDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsBedOccupancy.cs)_
- **BedNo**: `string`
- **BedStatus**: `string`
- **Ward**: `string`
- **HospitalName**: `string`

## dTBlackListPatientDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsBlacklistedPatients.cs)_
- **Username**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **IDNumber**: `string`
- **Telephone1**: `string`
- **DateTimeBlacklisted**: `DateTime`
- **Reason**: `string`
- **IsBlackListed**: `int`
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`

## dTBloodTransfusionDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsBloodTransfusion.cs)_
- **Name**: `string`
- **LetterHead**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **Telephone1**: `string`
- **AdmissionDateTime**: `DateTime`
- **DateTimePosted**: `DateTime`
- **AdmissionID**: `int`
- **BloodPressure**: `string`
- **Pulse**: `string`
- **Respiratory**: `string`
- **Temperature**: `string`
- **Comments**: `string`
- **Username**: `string`

## dTBookAdjustmentDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsBankRec.cs)_
- **SourceReference**: `string`
- **Description**: `string`
- **BankRecID**: `int`
- **FromDateTime**: `DateTime`
- **ToDateTime**: `DateTime`
- **BookBalance**: `double`
- **IsBookAdjustingItem**: `int`
- **IsIncrement**: `int`
- **IsAdjustment**: `int`
- **Amount**: `double`

## dTCancelledByDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsCancelledRcpts.cs)_
- **IssuedReceiptID**: `int`
- **IssuedReceiptNo**: `int`
- **DateTimeIssued**: `DateTime`
- **AmountPaid**: `double`
- **HasBeenCancelled**: `int`
- **CancelledBy**: `string`

## dTCancelledRcptsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsCancelledRcpts.cs)_
- **HospitalName**: `string`
- **IssuedReceiptID**: `int`
- **IssuedReceiptNo**: `int`
- **DateTimeIssued**: `DateTime`
- **AmountPaid**: `double`
- **PaymentMode**: `string`
- **HasBeenCancelled**: `int`
- **CancellationReason**: `string`
- **PaidInBy**: `string`
- **IssuedTo**: `string`
- **IssuedBy**: `string`

## dTCardexDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsCardex.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **PatientID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **AdmissionID**: `int`
- **AdmissionDateTime**: `DateTime`
- **AdmittingDoctor**: `string`
- **Residence**: `string`
- **DateTimePosted**: `DateTime`
- **Notes**: `string`
- **Username**: `string`
- **Telephone1**: `string`

## dTCashSaleByAccountDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsCashSalesByGrpAccount.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **SaleItemID**: `int`
- **Quantity**: `int`
- **Code**: `int`
- **Rate**: `double`
- **DiscountedAmount**: `double`
- **DateTimeSold**: `DateTime`
- **Expr1**: `string`
- **GroupAccountID**: `int`
- **Expr2**: `string`
- **HasBeenPaidFor**: `int`
- **IsCashSale**: `int`
- **CustomerName**: `string`

## dTCashierAdapterDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsCashierShiftEod.cs)_
- **TotalCollections**: `double`
- **Cash**: `double`
- **Mpesa**: `double`
- **DebitCard**: `double`
- **CreditCard**: `double`
- **Cheque**: `double`
- **DirectBank**: `double`
- **EFT**: `double`
- **AirtelMoney**: `double`
- **CashBoxTotals**: `double`
- **Notes**: `string`
- **BeginDateTime**: `DateTime`
- **EndDateTime**: `DateTime`
- **Name**: `string`
- **LetterHead**: `string`
- **Username**: `string`
- **IsOpen**: `int`

## dTCheckListAnaesthetistDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsCheckListAnaesthetist.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **AdmissionID**: `int`
- **BedID**: `int`
- **BedNo**: `string`
- **WardID**: `int`
- **Expr1**: `string`
- **Datetimeposted**: `DateTime`
- **Operation**: `string`
- **HB**: `string`
- **PCV**: `string`
- **Temp**: `string`
- **Albumin**: `string`
- **Sugar**: `string`
- **BP**: `string`
- **Pulse**: `string`
- **Weight**: `string`
- **Dentures**: `string`
- **MedicalHistory**: `string`
- **Allergies**: `string`
- **IsPremed**: `int`
- **PremedTime**: `string`
- **PremedType**: `string`
- **PremedAmount**: `string`
- **BloodAvailable**: `int`
- **BloodType**: `string`
- **Litres**: `string`
- **HasConsentGiven**: `int`
- **IsFitForOperation**: `int`
- **CertifiedBy**: `string`
- **SystemUserID**: `int`
- **Username**: `string`

## dTCheckListDoctorDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsCheckListDoctor.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **PatientID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **AdmissionID**: `int`
- **AdmissionDateTime**: `DateTime`
- **WardID**: `int`
- **Expr1**: `string`
- **BedID**: `int`
- **BedNo**: `string`
- **SystemUserID**: `int`
- **Username**: `string`
- **Datetimeposted**: `DateTime`
- **Operation**: `string`
- **HB**: `string`
- **PCV**: `string`
- **IsUrinalysisNormal**: `int`
- **ElectrocytesNormal**: `string`
- **Temp**: `string`
- **IsChestNormal**: `int`
- **BP**: `string`
- **Pulse**: `string`
- **MedicalHistory**: `string`
- **IsFitForOperation**: `int`
- **IsPremed**: `int`
- **PremedTime**: `string`
- **PremedType**: `string`
- **PremedAmount**: `string`
- **BloodAvailable**: `int`
- **BloodType**: `string`
- **Litres**: `string`
- **HasConsentGiven**: `int`
- **Anaesthetist**: `string`
- **CertifiedBy**: `string`

## dTCheckListNurseDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsCheckListNurse.cs)_
- **AdmissionID**: `int`
- **AdmissionDateTime**: `DateTime`
- **WardID**: `int`
- **Name**: `string`
- **BedID**: `int`
- **BedNo**: `string`
- **PatientID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **HospitalInfoID**: `int`
- **Expr1**: `string`
- **LetterHead**: `string`
- **TheatreChecklistNurseID**: `int`
- **DateTimePosted**: `DateTime`
- **Operation**: `string`
- **IsAppropriateGown**: `int`
- **Wigs**: `string`
- **Jewellery**: `string`
- **IDTag**: `string`
- **Dentures**: `string`
- **Prostheres**: `string`
- **IsShaving**: `int`
- **IsBladderEmpty**: `int`
- **IsCatheterization**: `int`
- **IsBowelEmpty**: `int`
- **IsEnema**: `int`
- **Starved**: `string`
- **Sugar**: `string`
- **Albumin**: `string`
- **Hb**: `string`
- **IsUreaTested**: `int`
- **BP**: `string`
- **Pulse**: `string`
- **FetalHeart**: `string`
- **IsInfusionGiven**: `int`
- **InfusionType**: `string`
- **InfusionAmount**: `string`
- **IsMedicationGiven24hrs**: `int`
- **MedType**: `string`
- **MedTime**: `string`
- **IsXrayTaken**: `int`
- **IsXrayWithPatient**: `int`
- **IsGastricLubeGiven**: `int`
- **GastricType**: `string`
- **GastricTime**: `string`
- **IsPremedication**: `int`
- **PremedType**: `string`
- **PremedTime**: `string`
- **CertifiedBy**: `string`
- **SystemUserID**: `int`
- **Username**: `string`

## dTChequeDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsCheque.cs)_
- **ChequeNo**: `string`
- **PaidTo**: `string`
- **AmountInWords**: `string`
- **DateTimePayable**: `DateTime`
- **Username**: `string`
- **SubAccountName**: `string`
- **MainAccountName**: `string`
- **TransactionDateTime**: `DateTime`
- **Description**: `string`
- **Amount**: `double`
- **EntryType**: `int`

## dTCollectionDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsCollections.cs)_
- **BatchID**: `int`
- **DateTimePosted**: `DateTime`
- **Username**: `string`
- **Name**: `string`
- **Amount**: `double`
- **Mpesa**: `double`
- **HospitalInfoID**: `int`
- **CompanyName**: `string`
- **LetterHead**: `string`

## dTComplaintsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPatientVisit.cs)_
- **Complaint**: `string`
- **ComplaintID**: `int`

## dTConsBillItemsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.HRDatasets/_DsConsBillItems.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Alias**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Designation**: `string`
- **MobileNo1**: `string`
- **DateTimeCreated**: `DateTime`
- **HospitalDeduction**: `double`
- **NetAmount**: `double`
- **TotalAmountPaid**: `double`
- **ConsultantBillID**: `int`
- **ConsultantID**: `int`
- **IsCleared**: `int`
- **TotalAmount**: `double`

## dTConsBillItemsStatusDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.HRDatasets/_DsConsBillItemsStatus.cs)_
- **ConsultantID**: `int`
- **Alias**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **MobileNo1**: `string`
- **DateTimeSold**: `DateTime`
- **ConsBillItemIsProcessed**: `int`
- **NetAmount**: `double`
- **ItemName**: `string`
- **HospitalName**: `string`
- **MedicalBillID**: `int`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **MedicalBillIsProcessed**: `bool`
- **MedicalBillNo**: `int`
- **CoverAmount**: `double`
- **DepositOffset**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **GroupAccountID**: `int`
- **Name**: `string`
- **CustomerName**: `string`
- **HasBeenPaidFor**: `int`
- **DateTimeSold1**: `DateTime`

## dTConsBillsByConsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.HRDatasets/_DsConsBillsByCons.cs)_
- **HospitalName**: `string`
- **ConsultantBillID**: `int`
- **PreparedBySysUID**: `int`
- **Surname**: `string`
- **MobileNo1**: `string`
- **ConsultantID**: `int`
- **DateTimeCreated**: `DateTime`
- **TotalAmount**: `double`
- **HospitalDeduction**: `double`
- **NetAmount**: `double`
- **IsCleared**: `int`
- **TotalAmountPaid**: `double`
- **PreparedBy**: `string`
- **ConsultantAlias**: `string`

## dTConsBillsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.HRDatasets/_DsConsBills.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Alias**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Designation**: `string`
- **MobileNo1**: `string`
- **DateTimeCreated**: `DateTime`
- **HospitalDeduction**: `double`
- **NetAmount**: `double`
- **TotalAmountPaid**: `double`
- **ConsultantBillID**: `int`
- **ConsultantID**: `int`
- **IsCleared**: `int`
- **TotalAmount**: `double`

## dTConsBookByConsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsConsBookingPerConsultant.cs)_
- **Name**: `string`
- **LetterHead**: `string`
- **DatetimeBooked**: `DateTime`
- **IsSeen**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **ConsultantID**: `int`
- **DateOfBirth**: `DateTime`
- **Telephone1**: `string`
- **Alias**: `string`
- **VisitDateTime**: `DateTime`

## dTConsentFormDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsConsentForm.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **PatientID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **AdmissionID**: `int`
- **BedID**: `int`
- **BedNo**: `string`
- **WardID**: `int`
- **Expr1**: `string`
- **AdmissionDateTime**: `DateTime`
- **AdmittingDoctor**: `string`
- **ReceivedByNurse**: `string`
- **OperationDate**: `DateTime`
- **Witness**: `string`
- **Operation**: `string`
- **TheatreQueueID**: `int`

## dTConsultantBookDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsConsultantBookings.cs)_
- **Name**: `string`
- **LetterHead**: `string`
- **DatetimeBooked**: `DateTime`
- **IsSeen**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Telephone1**: `string`
- **Alias**: `string`
- **VisitDateTime**: `DateTime`

## dTContinuationSheetDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsContinuationSheet.cs)_
- **PatientID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **BedID**: `int`
- **BedNo**: `string`
- **AdmissionDateTime**: `DateTime`
- **WardID**: `int`
- **Expr1**: `string`
- **AdmissionID**: `int`
- **dateTimePosted**: `DateTime`
- **Notes**: `string`
- **Username**: `string`

## dTCorporateDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsCorporateList.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **GroupAccountID**: `int`
- **groupAccount**: `string`
- **CreditLimit**: `float`
- **ContractAmount**: `double`
- **HasCoPay**: `int`
- **CoPayAmount**: `double`
- **HasVisitDaysCap**: `int`
- **Telephone1**: `string`
- **CappingDays**: `int`
- **IsActive**: `int`

## dTCreditNoteDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsCreditNote.cs)_
- **TransactionDateTime**: `DateTime`
- **SourceReference**: `string`
- **Description**: `string`
- **CreditNoteID**: `int`
- **CreditNoteNo**: `int`
- **CustomerName**: `string`
- **TelephoneNo**: `string`
- **Address**: `string`
- **EmailAddress**: `string`
- **TotalAmount**: `double`
- **Name**: `string`
- **LetterHead**: `string`
- **Username**: `string`

## dTCustomerDepositsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsIssuedReceipts.cs)_
- **IssuedReceiptID**: `int`
- **IssuedReceiptNo**: `int`
- **DateTimeIssued**: `DateTime`
- **AmountPaid**: `double`
- **IsCustomerDeposit**: `int`
- **SystemUserIDIssuedBy**: `int`
- **HasBeenCancelled**: `int`

## dTDbtPmtRcptDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsDebtorPmtRcpt.cs)_
- **HospitalName**: `string`
- **IssuedReceiptID**: `int`
- **IssuedReceiptNo**: `int`
- **DateTimeIssued**: `DateTime`
- **AmountPaid**: `double`
- **IssuedBy**: `string`
- **AmountReceived**: `double`
- **ChangeAmount**: `double`
- **PaidInBy**: `string`
- **PaymentFor**: `string`
- **IssuedTo**: `string`
- **PaymentMode**: `string`
- **LetterHead**: `string`
- **Description**: `string`

## dTDebtorsPaymentsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsIssuedReceipts.cs)_
- **IssuedReceiptID**: `int`
- **IssuedReceiptNo**: `int`
- **DateTimeIssued**: `DateTime`
- **AmountPaid**: `double`
- **IsCustomerDeposit**: `int`
- **ARInvoiceID**: `int`
- **HasBeenCancelled**: `int`
- **SystemUserIDIssuedBy**: `int`
- **IsDebtorPayment**: `int`

## dTDeliveryNoteDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsDeliveryNote.cs)_
- **DeliveryNoteID**: `int`
- **DateTimeCreated**: `DateTime`
- **CustomerName**: `string`
- **PhysicalAddress**: `string`
- **TelephoneNo1**: `string`
- **ReceivedBy**: `string`
- **DateTimeDelivered**: `DateTime`
- **Comment**: `string`
- **ItemName**: `string`
- **Quantity**: `int`
- **UnitOfMeasure**: `string`
- **Rate**: `double`
- **PerVAT**: `double`
- **PerDiscount**: `double`
- **Amount**: `double`
- **NetAmount**: `double`
- **VATTypeID**: `int`
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`

## dTDentalDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsDentalResultII.cs)_
- **VisitID**: `int`
- **Histoy**: `string`
- **Examinations**: `string`
- **Diagnosis**: `string`
- **TreatmentPlan**: `string`
- **TreatmentDone**: `string`
- **IsDental**: `int`
- **DatePosted**: `DateTime`
- **Name**: `string`
- **Age**: `int`
- **VisitDateTime**: `DateTime`
- **DateTimeRequested**: `DateTime`
- **Surname**: `string`
- **OtherNames**: `string`
- **LetterHead**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **IDNumber**: `string`
- **OutPatientNo**: `int`
- **Residence**: `string`
- **GroupAccountID**: `int`
- **Expr1**: `string`
- **DoctorID**: `int`
- **Expr2**: `string`
- **Registration**: `string`

## dTDentalExaminationDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsDentalExamination.cs)_
- **MedReqOExamID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Age**: `int`
- **Sex**: `string`
- **TelephoneNo**: `string`
- **PatientComplaints**: `string`
- **Findings**: `string`
- **Impression**: `string`
- **Comments**: `string`
- **DatePosted**: `DateTime`
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Residence**: `string`
- **Expr1**: `int`

## dTDentalResultDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsDentalResults.cs)_
- **PatientComplaints**: `string`
- **Findings**: `string`
- **Impression**: `string`
- **Comments**: `string`
- **DatePosted**: `DateTime`
- **VisitID**: `int`
- **Age**: `int`
- **AgeMonths**: `int`
- **AgeWeeks**: `int`
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **SystemUserID**: `int`
- **DateTimeRequested**: `DateTime`
- **OutPatientNo**: `int`
- **TelephoneNo**: `string`
- **DentalResultsID**: `int`
- **MedReqOExamID**: `int`
- **Username**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Expr1**: `int`
- **Expr2**: `int`
- **Sex**: `string`

## dTDentistExaminationDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsDentistExamination.cs)_
- **Name**: `string`
- **LetterHead**: `string`
- **VisitDateTime**: `DateTime`
- **MedReqOExamID**: `int`
- **DateTimeRequested**: `DateTime`
- **Surname**: `string`
- **OutPatientNo**: `int`
- **OtherNames**: `string`
- **Age**: `int`
- **Sex**: `string`
- **TelephoneNo**: `string`
- **Findings**: `string`
- **Impression**: `string`
- **Examiner**: `string`
- **Center**: `string`
- **PatientComplaints**: `string`
- **Comments**: `string`
- **DatePosted**: `DateTime`
- **VisitID**: `int`
- **HospitalInfoID**: `int`
- **Expr1**: `int`

## dTDepSumDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsIssuedReceiptsAllUsers.cs)_
- **IssuedReceiptID**: `int`
- **DateTimeIssued**: `DateTime`
- **AmountPaid**: `double`
- **IsCashSale**: `int`
- **IsCustomerDeposit**: `int`
- **Description**: `string`
- **ItemCategory**: `string`
- **Department**: `string`
- **HasBeenCancelled**: `int`
- **ItemName**: `string`
- **DiscountedAmount**: `double`
- **SaleItemID**: `int`
- **MedicalBillID**: `int`
- **Quantity**: `int`
- **Rate**: `double`
- **PercentageDiscount**: `double`
- **Amount**: `double`
- **DateTimeSold**: `DateTime`
- **SystemUserID**: `int`
- **IssuedReceiptNo**: `int`
- **HospitalName**: `string`
- **IssuedBySysUser**: `string`
- **PaidInBy**: `string`

## dTDepSummaryDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsIssuedReceipts.cs)_
- **IssuedReceiptID**: `int`
- **IssuedReceiptNo**: `int`
- **DateTimeIssued**: `DateTime`
- **AmountPaid**: `double`
- **SystemUserIDIssuedBy**: `int`
- **IsCustomerDeposit**: `int`
- **DepartmentName**: `string`
- **ItemCategoryName**: `string`
- **IssuedBy**: `string`
- **HasBeenCancelled**: `int`
- **ItemName**: `string`
- **IsCashSale**: `int`
- **DiscountedAmount**: `double`
- **ARInvoiceID**: `int`

## dTDiabetesMonitorDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsDiabetesMonitor.cs)_
- **Name**: `string`
- **LetterHead**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **Telephone1**: `string`
- **AdmissionDateTime**: `DateTime`
- **AdmissionID**: `int`
- **DateTimePosted**: `DateTime`
- **RBS**: `string`
- **FBS**: `string`
- **Intervention**: `string`
- **Username**: `string`

## dTDiagnosisDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPatientVisit.cs)_
- **Age**: `int`
- **VisitDateTime**: `DateTime`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **ThirdName**: `string`
- **Diagnosis**: `string`
- **VisitID**: `int`
- **DiagnosisID**: `int`

## dTDischargeBillsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsDischargedPatBills.cs)_
- **HospitalName**: `string`
- **IsInAdmission**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **BedNo**: `string`
- **AdmissionID**: `int`
- **IsCurrentBed**: `int`
- **AdmissionDateTime**: `DateTime`
- **Ward**: `string`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **CoverAmount**: `double`
- **DepositOffset**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **DepositBalance**: `double`
- **GroupAccount**: `string`
- **DischargeDateTime**: `DateTime`

## dTDischargeSummaryDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsDischargeSummary.cs)_
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **VisitID**: `int`
- **AdmissionDateTime**: `DateTime`
- **DischargeDateTime**: `DateTime`
- **Diagnosis**: `string`
- **History**: `string`
- **ExaminationFindings**: `string`
- **InvestigationsResults**: `string`
- **TreatmentGiven**: `string`
- **DischargePrescription**: `string`
- **Comments**: `string`
- **NextAppointmentDateTime**: `DateTime`
- **AdmissionID**: `int`
- **HospitalName**: `string`
- **LetterHead**: `string`
- **HasNextAppointment**: `int`
- **DischargedBySysUserID**: `int`
- **AmittedByUsername**: `string`
- **AdmittingDoctor**: `string`
- **DischargingDoctor**: `string`
- **InPatientNo**: `int`
- **DateOfBirth**: `DateTime`
- **Admittedduration**: `string`
- **IsReferal**: `int`
- **IsAlive**: `int`

## dTDischargeSummaryIIDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsDischargeSummaryII.cs)_
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **VisitID**: `int`
- **AdmissionDateTime**: `DateTime`
- **DischargeDateTime**: `DateTime`
- **Diagnosis**: `string`
- **History**: `string`
- **ExaminationFindings**: `string`
- **InvestigationsResults**: `string`
- **TreatmentGiven**: `string`
- **DischargePrescription**: `string`
- **Comments**: `string`
- **NextAppointmentDateTime**: `DateTime`
- **AdmissionID**: `int`
- **HospitalName**: `string`
- **LetterHead**: `string`
- **HasNextAppointment**: `int`
- **DischargedBySysUserID**: `int`
- **AmittedByUsername**: `string`
- **AdmittingDoctor**: `string`
- **DischargingDoctor**: `string`
- **Admittedduration**: `string`
- **DateOfBirth**: `DateTime`
- **IsReferal**: `int`
- **IsAlive**: `int`
- **InPatientNo**: `int`

## dTDiseasePrevalenceByImpressionDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.MedicalDatasets/_DsDiseasePrevalenceByImpression.cs)_
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **VisitDateTime**: `DateTime`
- **Age**: `int`
- **AgeMonths**: `int`
- **AgeWeeks**: `int`
- **Impression**: `string`
- **VisitID**: `int`
- **HospitalName**: `string`

## dTDispensedDrugsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsDispensedDrugs.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **SaleItemID**: `int`
- **Code**: `int`
- **Quantity**: `int`
- **DateTimeSold**: `DateTime`
- **Expr1**: `string`
- **Username**: `string`
- **Rate**: `double`
- **HasBeenDispensed**: `int`
- **Amount**: `double`
- **DiscountedAmount**: `double`

## dTDoctorNotesDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsDoctorNotes.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Username**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **AdmissionDateTime**: `DateTime`
- **dateTimePosted**: `DateTime`
- **Notes**: `string`
- **AdmissionID**: `int`

## dTDonationDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsDonors.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **DonorID**: `int`
- **Donor**: `string`
- **Contact**: `string`
- **PhysicalLocation**: `string`
- **DonorTypeID**: `int`
- **DonorTypeName**: `string`
- **DonationID**: `int`
- **AmountDonated**: `double`
- **DateTimeDonated**: `DateTime`
- **DeadlineDateTime**: `DateTime`
- **AmountUsed**: `double`
- **DonationExpenditureID**: `int`
- **Amount**: `double`
- **DateTimeUsed**: `DateTime`
- **ApprovedBy**: `string`
- **Purpose**: `string`

## dTEODDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsEOD.cs)_
- **Name**: `string`
- **LetterHead**: `string`
- **EODID**: `int`
- **ShiftID**: `int`
- **TotalCollections**: `double`
- **Cash**: `double`
- **Mpesa**: `double`
- **DebitCard**: `double`
- **CreditCard**: `double`
- **Cheque**: `double`
- **DirectBank**: `double`
- **EFT**: `double`
- **AirtelMoney**: `double`
- **CashBoxTotals**: `double`
- **Notes**: `string`
- **SystemUserID**: `int`
- **BeginDateTime**: `DateTime`
- **EndDateTime**: `DateTime`
- **IsOpen**: `int`
- **Username**: `string`

## dTEOSRDataTableDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsEOSR.cs)_
- **Username**: `string`
- **Amount**: `double`
- **SystemUserID**: `int`
- **EntryType**: `int`
- **SubAccountName**: `string`
- **AccountName**: `string`
- **AccountType**: `string`
- **AccountID**: `int`

## dTEOSRMainDataTableDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsEOSR.cs)_
- **Name**: `string`
- **LetterHead**: `string`
- **BeginDateTime**: `DateTime`
- **EndDateTime**: `DateTime`
- **OpeningBalance**: `double`
- **ExpectedClosingBalance**: `double`
- **NetCashTransactions**: `double`
- **ActualBalance**: `double`
- **BalanceDifference**: `double`
- **Explanation**: `string`
- **LetterHead1**: `string`
- **OpeningBalance1**: `float`
- **ExpectedClosingBalance1**: `float`
- **NetCashTransactions1**: `float`
- **ActualBalance1**: `float`
- **BalanceDifference1**: `float`

## dTEmployeesDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.HRDatasets/_DsEmployees.cs)_
- **HospitalName**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **StaffNo**: `string`
- **IDNo**: `string`
- **DateEmployed**: `DateTime`
- **EmploymentType**: `string`
- **Designation**: `string`
- **Department**: `string`
- **PayrollParameter**: `string`
- **ParameterCategory**: `string`
- **EmployeeID**: `int`
- **BasicPay**: `double`

## dTExpensesDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsExpenses.cs)_
- **Name**: `string`
- **Description**: `string`
- **TotalAmount**: `double`
- **TotalAmountPaid**: `double`
- **Balance**: `double`
- **DateTimeIncurred**: `DateTime`
- **DateDue**: `DateTime`
- **ExpenseID**: `int`
- **HospitalName**: `string`
- **LetterHead**: `string`
- **AccountType**: `string`
- **AccountNo**: `int`
- **AccountName**: `string`
- **AccSubAccID**: `int`
- **SourceReference**: `string`
- **EntryType**: `int`
- **SubAccountName**: `string`
- **DateTimePosted**: `DateTime`
- **AmountPosted**: `double`
- **TransactionAmount**: `double`
- **JournalVoucherID**: `int`
- **TransactionDateTime**: `DateTime`

## dTFamSocEcoHistoryDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPatientVisit.cs)_
- **MedFamSocioEcoHistory**: `string`
- **VisitID**: `int`

## dTFamilySocEconHisDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPatientHistory.cs)_
- **FamilySocioEconomic**: `string`

## dTFinancialDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsFinancialStatements.cs)_
- **OpenDate**: `DateTime`
- **CloseDate**: `DateTime`
- **FinancialID**: `int`
- **StatementDate**: `DateTime`
- **Cash**: `double`
- **AccountReceivable**: `double`
- **Inventory**: `double`
- **OtherCurrentAssets**: `double`
- **Land**: `double`
- **Buildings**: `double`
- **AccumulatedDepreciation**: `double`
- **OtherAssets**: `double`
- **AccountsPayable**: `double`
- **AccruedLiabilities**: `double`
- **AccruedIncomeTaxes**: `double`
- **DeferredIncomeTaxes**: `double`
- **NotesPayable**: `double`
- **Bank**: `double`
- **PreferredStock**: `double`
- **RetainedEarnings**: `double`
- **CommonStock**: `double`
- **NetSales**: `double`
- **CostOfGoodsSold**: `double`
- **InterestExpenses**: `double`
- **SellingAdminGeneralExpenses**: `double`
- **OtherIncomeExpenses**: `double`
- **Taxes**: `double`
- **FiscalPeriodID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **CustomerDeposits**: `double`
- **LongTermDebts**: `double`
- **IncomeTaxes**: `double`
- **Equipment**: `double`
- **OtherIncome**: `double`
- **DepreciationExpenses**: `double`
- **FromDateTime**: `DateTime`
- **ToDateTime**: `DateTime`
- **OpeningBalanceEquity**: `double`
- **MotorVehicle**: `double`
- **Furniture**: `double`
- **FixturesAndFittings**: `double`
- **OtherCurrentLiabilities**: `double`

## dTFluidMonitorDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsFluidMonitor.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **Telephone1**: `string`
- **AdmissionID**: `int`
- **AdmissionDateTime**: `DateTime`
- **AdmittingDoctor**: `string`
- **Username**: `string`
- **FluidsMonitorID**: `int`
- **DateTimePosted**: `DateTime`
- **IVFluids**: `double`
- **NGT**: `double`
- **Vomitus**: `double`
- **Urine**: `double`
- **TotalInput**: `double`
- **TotalOutPut**: `double`

## dTGExaminationsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPatientVisit.cs)_
- **NurseTriageID**: `int`
- **VisitID**: `int`
- **Temperature**: `string`
- **TemperatureRemarks**: `string`
- **Weight**: `string`
- **WeightRemarks**: `string`
- **BloodPressure**: `string`
- **BloodPressureRemarks**: `string`
- **RespirationRate**: `string`
- **RespirationRateRemarks**: `string`
- **PulseRate**: `string`
- **PulseRateRemarks**: `string`
- **Notes**: `string`

## dTGLedgerDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsGLedger.cs)_
- **Amount**: `double`
- **AccountType**: `string`
- **TransactionDateTime**: `DateTime`
- **MainAccountName**: `string`
- **SubAccountName**: `string`
- **HospitalName**: `string`
- **LetterHead**: `string`
- **AccSubAccID**: `int`
- **SubAccountID**: `int`
- **NetBalance**: `double`
- **SourceReference**: `string`
- **Description**: `string`
- **EntryType**: `int`
- **AccountNo**: `int`
- **JournalVoucherID**: `int`
- **OpenDate**: `DateTime`
- **CloseDate**: `DateTime`
- **FromDateTime**: `DateTime`
- **ToDateTime**: `DateTime`
- **Username**: `string`

## dTGRNDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.ProcurementDatasets/_DsGRN.cs)_
- **HospitalName**: `string`
- **GRNID**: `int`
- **APInvoiceNo**: `string`
- **DeliveryNoteNo**: `string`
- **HasBeenChecked**: `int`
- **HasBeenReceived**: `int`
- **IsCommittedToStock**: `int`
- **Name**: `string`
- **Description**: `string`
- **Quality**: `string`
- **UnitOfMeasure**: `string`
- **QuantityReceived**: `int`
- **Rate**: `double`
- **PerVAT**: `double`
- **VATInclusiveAmount**: `double`
- **PerDiscount**: `double`
- **NetAmount**: `double`
- **EarliestExpiryDate**: `DateTime`
- **BatchNo**: `string`
- **QuantityOrdered**: `int`
- **PurchaseOrderNo**: `int`
- **SupplierName**: `string`
- **SupplierPhysicalAddress**: `string`
- **SupplierTown**: `string`
- **SupplierPostalAddress**: `string`
- **SupplierPostalCode**: `string`
- **SupplierTelephone1**: `string`
- **SupplierEmailAddress**: `string`
- **LetterHead**: `string`

## dTGatePassDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsGatePass.cs)_
- **ARInvoiceID**: `int`
- **OutPatientNo**: `int`
- **PatientName**: `string`
- **DateTimePosted**: `DateTime`
- **Name**: `string`
- **LetterHead**: `string`
- **GroupAccountID**: `int`
- **Expr1**: `string`

## dTIOIssuanceDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.ProcurementDatasets/_DsIOIssuance.cs)_
- **HospitalName**: `string`
- **DateTimeDispatched**: `DateTime`
- **ItemsDispatchedBy**: `string`
- **InternalOrderItemID**: `int`
- **ProductID**: `int`
- **QuantityOrdered**: `int`
- **QuantityIssued**: `int`
- **UnitOfMeasure**: `string`
- **UnitCost**: `double`
- **UnitPrice**: `double`
- **ItemName**: `string`
- **OrderStatus**: `string`
- **IssuingLocation**: `string`
- **RequestingLocation**: `string`
- **IssuingStorageLocationID**: `int`
- **OrderItemsDispatched**: `int`
- **IsReturnedStock**: `int`

## dTImpressionDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPatientVisit.cs)_
- **Description**: `string`
- **ImpressionID**: `int`

## dTInPatientRegisterDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsInPatientRegister.cs)_
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **Age**: `int`
- **AgeMonths**: `int`
- **AgeWeeks**: `int`
- **HospitalName**: `string`
- **LetterHead**: `string`
- **Diagnosis**: `string`
- **AdmissionID**: `int`
- **VisitID**: `int`
- **AdmittingDoctor**: `string`
- **AdmissionDateTime**: `DateTime`
- **DischargeDateTime**: `DateTime`
- **IsInAdmission**: `int`
- **InPatientNo**: `int`
- **GroupAccount**: `string`
- **DischargingDoctor**: `string`

## dTInPatientsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsInPatientBills.cs)_
- **HospitalName**: `string`
- **IsInAdmission**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **BedNo**: `string`
- **AdmissionID**: `int`
- **IsCurrentBed**: `int`
- **AdmissionDateTime**: `DateTime`
- **Ward**: `string`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **CoverAmount**: `double`
- **DepositOffset**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **DepositBalance**: `double`
- **GroupAccount**: `string`

## dTInpatientBillsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatBills/_DsMedicalBillsInpatient.cs)_
- **VisitID**: `int`
- **DateTimeCreated**: `DateTime`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **IsProcessed**: `bool`
- **MedicalBillNo**: `int`
- **CustomerName**: `string`
- **CoverAmount**: `double`
- **DepositOffset**: `double`
- **WriteOffAmount**: `double`
- **SalesDiscountAmount**: `double`
- **DepositBalance**: `double`
- **GroupAccount**: `string`
- **AdmissionDateTime**: `DateTime`
- **IsInAdmission**: `int`
- **AdmissionID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **OutPatientNo**: `int`
- **InPatientNo**: `int`

## dTInpatientPrescriptionDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsInpatientDispensedItems.cs)_
- **Name**: `string`
- **Username**: `string`
- **HospitalInfoID**: `int`
- **Expr1**: `string`
- **LetterHead**: `string`
- **DateTimeSold**: `DateTime`
- **Quantity**: `int`
- **DateTimeCreated**: `DateTime`
- **CustomerName**: `string`
- **VisitID**: `int`
- **MedicalBillID**: `int`

## dTInpatientVitalDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsInpatientVitals.cs)_
- **PatientID**: `int`
- **AdmissionDateTime**: `DateTime`
- **VitalType**: `string`
- **Value**: `string`
- **DateTimePosted**: `DateTime`
- **Comment**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **NextOfKin**: `string`
- **NextOfKinRelationship**: `string`
- **NextOfKinContact**: `string`
- **Username**: `string`
- **Name**: `string`
- **LetterHead**: `string`
- **AdmissionID**: `int`

## dTInternalOrderDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.ProcurementDatasets/_DsInternalOrder.cs)_
- **OrderStatus**: `string`
- **IssuingLocationComment**: `string`
- **DateTimeSent**: `DateTime`
- **ItemsReceived**: `int`
- **Item**: `string`
- **UnitDefination**: `string`
- **InternalOrderID**: `int`
- **HospitalName**: `string`
- **DateTimeReceived**: `DateTime`
- **HasBeenApproved**: `int`
- **DateTimeDispatched**: `DateTime`
- **OrderItemsDispatched**: `int`
- **QuantityOrdered**: `int`
- **QuantityIssued**: `int`
- **HasBeenSent**: `int`
- **ItemsReceivedBySysUserID**: `int`
- **OrderItemsReceivedBy**: `string`
- **EarliestExpiryDate**: `DateTime`
- **IssuedTotalPackedQuantity**: `int`
- **UnitOfMeasure**: `string`
- **UnitCost**: `float`
- **UnitPrice**: `float`
- **InternalOrderItemID**: `int`
- **UnitCost1**: `double`
- **UnitPrice1**: `double`
- **IsReturnedStock**: `int`
- **RequestingLocationComment**: `string`

## dTIssRcptsAllUsersDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsIssuedReceiptsAllUsers.cs)_
- **HospitalName**: `string`
- **IssuedReceiptID**: `int`
- **IssuedReceiptNo**: `int`
- **DateTimeIssued**: `DateTime`
- **AmountPaid**: `double`
- **PaidInBy**: `string`
- **IssuedBy**: `string`
- **PaymentMode**: `string`
- **PaymentModeCategory**: `string`
- **HasBeenCancelled**: `int`

## dTIssuedReceiptsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsIssuedReceipts.cs)_
- **HospitalName**: `string`
- **IssuedReceiptNo**: `int`
- **DateTimeIssued**: `DateTime`
- **AmountPaid**: `double`
- **SystemUserIDIssuedBy**: `int`
- **PaymentFor**: `string`
- **PaymentMode**: `string`
- **PaymentModeCategory**: `string`
- **PaidInBy**: `string`
- **IssuedBy**: `string`
- **IsCustomerDeposit**: `int`
- **HasBeenCancelled**: `int`
- **CancellationReason**: `string`
- **IssuedReceiptID**: `int`
- **IsDebtorPayment**: `int`

## dTIssuingStorageLocDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.ProcurementDatasets/_DsInternalOrder.cs)_
- **InternalOrderID**: `int`
- **IssuingStorageLocationID**: `int`
- **IssuingLocation**: `string`
- **DispatchedBy**: `string`

## dTJustineDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsSplitChequeItem.cs)_
- **Name**: `string`
- **LetterHead**: `string`
- **ChequeID**: `int`
- **PaidTo**: `string`
- **Amount**: `double`
- **AmountInWords**: `string`
- **DateTimePayable**: `DateTime`
- **ChequeNo**: `string`
- **BankName**: `string`
- **SplitChequeitemID**: `int`

## dTKitchenOrder1DataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsKitchenOrder1.cs)_
- **HospitalName**: `string`
- **CustomerName**: `string`
- **DateTimeCreated**: `DateTime`
- **IsProcessed**: `int`
- **SalesOrderID**: `int`
- **StorageLocationID**: `int`
- **ItemCategoryID**: `int`
- **DepartmentID**: `int`
- **ItemName**: `string`
- **Code**: `int`
- **QuantityOrdered**: `int`
- **Rate**: `double`
- **PercentageVAT**: `double`
- **Amount**: `double`
- **PercentageDiscount**: `double`
- **NetAmount**: `double`
- **SalesOrderItemID**: `int`
- **CreatedBySysUID**: `int`
- **Username**: `string`
- **LetterHead**: `string`

## dTLabDataSummaryDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.Lab/_DsLabDataSummary.cs)_
- **Test**: `string`
- **TestComponent**: `string`
- **Total**: `int`
- **MaleTotal**: `int`
- **FemaleTotal**: `int`
- **LessThan5Pos**: `int`
- **Btn5And14Pos**: `int`
- **GreaterThan14Pos**: `int`
- **LessThan5Tested**: `int`
- **Btn5And14Tested**: `int`
- **GreaterThan14Tested**: `int`
- **VeryLow**: `int`
- **Low**: `int`
- **Normal**: `int`
- **High**: `int`
- **ToDateTime**: `DateTime`
- **LetterHead**: `string`
- **LabDataSummaryID**: `int`
- **HospitalName**: `string`
- **FromDateTime**: `DateTime`

## dTLabRequestDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPatientVisit.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Doctor**: `string`
- **IsOutPatient**: `int`
- **DateTimeRequested**: `DateTime`
- **IsDone**: `int`
- **DateTimeDone**: `DateTime`
- **Surname**: `string`
- **OtherNames**: `string`
- **Age**: `int`
- **Sex**: `string`
- **IsSelfRequest**: `int`
- **Technologist**: `string`
- **ReasonNotDone**: `string`
- **AgeMonths**: `int`
- **AgeWeeks**: `int`
- **MedReqTestItemID**: `int`
- **Test**: `string`
- **Conclusion**: `string`
- **MedicalBillID**: `int`
- **DateTimeCreated**: `DateTime`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **GroupAccountID**: `int`
- **GroupAccount**: `string`
- **VisitID**: `int`
- **MedReqTestID**: `int`
- **IsInternal**: `int`
- **RequestedByID**: `int`
- **RequestedBy**: `string`
- **Value**: `string`
- **Units**: `string`
- **TestControl**: `string`
- **TestComponent**: `string`
- **HospitalName**: `string`
- **Specimen**: `string`
- **Remark**: `string`
- **OutPatientNo**: `int`
- **NormalRange**: `string`
- **Telephone1**: `string`
- **Residence**: `string`
- **CityTown**: `string`
- **TestID**: `int`

## dTLessThan7DaysDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsLessThan7DaysVisit.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **Residence**: `string`
- **Telephone1**: `string`
- **DateTimePosted**: `DateTime`
- **Username**: `string`
- **Reason**: `string`
- **LastVisitDateTime**: `DateTime`

## dTLockedBillsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsLockedMedicalBills.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **DatetimeLocked**: `DateTime`
- **IsLocked**: `int`
- **SystemUserID**: `int`
- **Username**: `string`
- **DateTimeCreated**: `DateTime`
- **TotalBillAmount**: `float`
- **AdvancePayment**: `float`
- **TotalAmountPaid**: `float`
- **CustomerName**: `string`
- **CoverAmount**: `double`
- **SalesDiscountAmount**: `double`
- **DepositOffset**: `double`
- **WriteOffAmount**: `double`
- **DepositBalance**: `double`
- **GroupAccountID**: `int`
- **Expr1**: `string`
- **PledgeDate**: `DateTime`
- **Telephone**: `string`
- **Name1**: `string`

## dTLockedProductDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsLockedProducts.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **ProductID**: `int`
- **ProductName**: `string`
- **UnitCost**: `double`
- **UnitPrice**: `double`
- **GroupAccountID**: `int`
- **groupAccount**: `string`
- **LetterHead**: `string`

## dTLockedServiceDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsLockedServices.cs)_
- **CashRate**: `double`
- **ServiceID**: `int`
- **Name**: `string`
- **GroupAccountID**: `int`
- **groupAccount**: `string`
- **HospitalInfoID**: `int`
- **hospitalName**: `string`
- **LetterHead**: `string`

## dTMaternityBeheadDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsMaternityFile.cs)_
- **Name**: `string`
- **LetterHead**: `string`
- **AdmissionDateTime**: `DateTime`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **Telephone1**: `string`
- **AdmissionID**: `int`
- **DateTimePosted**: `DateTime`
- **Para**: `string`
- **Gravida**: `string`
- **Clinic**: `string`
- **LMP**: `string`
- **EDD**: `string`
- **PeriodOfGestation**: `string`
- **Occupation**: `string`
- **Diagnosis**: `string`
- **EducationLevel**: `string`
- **Username**: `string`

## dTMaternityFamilyHistoDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsMaternityFamilyHistory.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **PatientID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **AdmissionID**: `int`
- **DOB**: `DateTime`
- **Place**: `string`
- **DurationOfLabor**: `string`
- **Delivery**: `string`
- **Weight**: `string`
- **Expr1**: `string`
- **IsAlive**: `int`
- **Feeding**: `string`
- **Puerparium**: `string`
- **Assessment**: `string`
- **Username**: `string`

## dTMaximumPrescribedQtyDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsMaximumPrescribedQty.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **ProductID**: `int`
- **Expr1**: `string`
- **UnitCost**: `double`
- **UnitPrice**: `double`
- **MaximumPrescriptionQty**: `int`

## dTMedicalBilDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsMedicalBillInPatient.cs)_
- **DateTimeCreated**: `DateTime`
- **AdvancePayment**: `float`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **MedicalBillNo**: `int`
- **CustomerName**: `string`
- **CoverAmount**: `double`
- **DepositOffset**: `double`
- **Surname**: `string`
- **OtherNames**: `string`
- **DepositBalance**: `double`
- **Age**: `int`
- **VisitDateTime**: `DateTime`
- **LetterHead**: `string`
- **AdmissionDateTime**: `DateTime`
- **DischargeDateTime**: `DateTime`
- **AdmittingDoctor**: `string`
- **AdmissionID**: `int`
- **WriteOffAmount**: `double`
- **SalesDiscountAmount**: `double`
- **Name**: `string`
- **ARInvoiceNo**: `int`
- **IsInAdmission**: `int`
- **Admittedduration**: `string`
- **IsProcessed**: `int`

## dTMedicalBillARInvoiceBBDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsMedicalBillsARInvoiceB.cs)_
- **ARInvoiceID**: `int`
- **ARInvoiceNo**: `int`
- **ARInvoiceDateTimeCreated**: `DateTime`
- **DueDate**: `DateTime`
- **ARInvoiceAmountReceivable**: `double`
- **IsPaid**: `int`
- **InvoiceTo**: `string`
- **Address**: `string`
- **Telephone1**: `string`
- **Telephone2**: `string`
- **EmailAddress**: `string`
- **ARInvoiceTotalAmountPaid**: `double`
- **Code**: `int`
- **Name**: `string`
- **Description**: `string`
- **Quantity**: `int`
- **Rate**: `double`
- **VAT**: `double`
- **PercentageDiscount**: `double`
- **Amount**: `double`
- **DiscountedAmount**: `double`
- **MedicalBillNo**: `int`
- **BillDateTimeCreated**: `DateTime`
- **CustomerName**: `string`
- **HospitalName**: `string`
- **LetterHead**: `string`
- **TotalBillAmount**: `float`
- **BillTotalAmountPaid**: `float`
- **PreparedBy**: `string`
- **SaleItemARInvoiceID**: `int`
- **CoverAmount**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **ItemCategoryID**: `int`
- **DepartmentID**: `int`
- **ItemCategory**: `string`
- **CreditNoteAmount**: `double`
- **CreditNoteReason**: `string`
- **OrderNo**: `string`
- **OutPatientNo**: `int`
- **CoverAmount1**: `double`
- **Description1**: `string`
- **CoverAmount2**: `double`
- **Description2**: `string`
- **DateTimeOfAdmission**: `DateTime`
- **DateTimeOfDischarge**: `DateTime`
- **Expr1**: `int`
- **InPatientNo**: `int`
- **DoctorName**: `string`
- **Sponsor**: `string`
- **PrincipalMember**: `string`
- **MembershipNo**: `string`
- **CompanyName**: `string`
- **Terms**: `string`

## dTMedicalBillDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsMedicalBill.cs)_
- **DateTimeCreated**: `DateTime`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **MedicalBillNo**: `int`
- **Age**: `int`
- **LetterHead**: `string`
- **HospitalName**: `string`
- **VisitDateTime**: `DateTime`
- **MedicalBillID**: `int`
- **VisitID**: `int`
- **IsProcessed**: `bool`
- **DateTimeProcessed**: `string`
- **CoverAmount**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **DepositOffset**: `double`
- **DepositBalance**: `double`
- **GroupAccountID**: `int`
- **Name**: `string`
- **Telephone1**: `string`

## dTMedicalBillPaymentDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsMedicalBill.cs)_
- **Username**: `string`
- **IssuedReceiptNo**: `int`
- **AmountReceived**: `double`
- **ChangeAmount**: `double`
- **AmountPaid**: `double`
- **PaymentFor**: `string`
- **IssuedTo**: `string`
- **PaymentModeID**: `int`
- **IssuedReceiptID**: `int`
- **PaidInBy**: `string`
- **DateTimeIssued**: `DateTime`
- **SystemUserID**: `int`
- **MedicalBillID**: `int`
- **MedicalBillNo**: `int`
- **PaymentMode**: `string`
- **HospitalName**: `string`
- **LetterHead**: `string`
- **Description**: `string`
- **IsCustomerDeposit**: `int`
- **IssuedByUserName**: `string`
- **HasBeenCancelled**: `int`

## dTMedicalBillsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsMedicalBills.cs)_
- **LetterHead**: `string`
- **VisitID**: `int`
- **DateTimeCreated**: `DateTime`
- **TotalBillAmount**: `double`
- **TotalAmountPaid**: `double`
- **Balance**: `double`
- **MedicalBillNo**: `int`
- **HospitalName**: `string`
- **GroupAccountName**: `string`
- **CustomerName**: `string`
- **Code**: `int`
- **Name**: `string`
- **Description**: `string`
- **Quantity**: `int`
- **Rate**: `double`
- **PercentageDiscount**: `double`
- **Amount**: `double`
- **DiscountedAmount**: `double`
- **VAT**: `double`
- **OutPatientNo**: `int`
- **SaleItemID**: `int`
- **AdmissionID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **IsProcessed**: `bool`
- **DepositBalance**: `double`
- **WriteOffAmount**: `double`
- **SalesDiscountAmount**: `double`
- **CoverAmount**: `double`
- **DepositOffset**: `double`

## dTMedicalSurgicalHistoryDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPatientVisit.cs)_
- **Description**: `string`
- **VisitID**: `int`

## dTMedicalsurgicalhistoriesDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPatientHistory.cs)_
- **MedicalSurgicalHistory**: `string`

## dTNurseCarePlanDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsNurseCarePlan.cs)_
- **AdmissionID**: `int`
- **AdmissionDateTime**: `DateTime`
- **DischargeDateTime**: `DateTime`
- **AdmittingDoctor**: `string`
- **DateTimePosted**: `DateTime`
- **Expr1**: `int`
- **Assessment**: `string`
- **NursingDiagnosis**: `string`
- **ExpectedOutcome**: `string`
- **NursingInterventions**: `string`
- **ScientificRationale**: `string`
- **Implementation**: `string`
- **Evaluation**: `string`
- **Username**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **Diagnosis**: `string`
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`

## dTOExaminationDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsOExamination.cs)_
- **HospitalName**: `string`
- **LetterHead**: `string`
- **VisitID**: `int`
- **VisitDateTime**: `DateTime`
- **Surname**: `string`
- **OtherNames**: `string`
- **OutPatientNo**: `int`
- **Age**: `int`
- **Sex**: `string`
- **TelephoneNo**: `string`
- **PostalAddress**: `string`
- **EmailAddress**: `string`
- **PostalCode**: `string`
- **History**: `string`
- **TechniqueProcedure**: `string`
- **Findings**: `string`
- **Impression**: `string`
- **Comment**: `string`
- **Examiner**: `string`
- **Center**: `string`
- **DateTimeDone**: `DateTime`
- **IsDone**: `int`
- **ReasonNotDone**: `string`
- **IsInternal**: `int`
- **RequestedByUsername**: `string`
- **Examination**: `string`
- **DateTimeRequested**: `DateTime`
- **MedReqOExamID**: `int`

## dTOPDBillByGrpProcDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatBills/_DsOutPatBillsProcByGrpAcc.cs)_
- **DateTimeCreated**: `DateTime`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **IsProcessed**: `bool`
- **MedicalBillNo**: `int`
- **CoverAmount**: `double`
- **DepositOffset**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **DepositBalance**: `double`
- **Surname**: `string`
- **OtherNames**: `string`
- **HospitalName**: `string`
- **VisitID**: `int`
- **MedicalBillID**: `int`
- **AdmissionID**: `int`
- **OutPatientNo**: `int`
- **Doctor**: `string`
- **GroupAccountID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **TelephoneNo**: `string`
- **IDNumber**: `string`
- **CustomerName**: `string`
- **ARInvoiceID**: `int`
- **ARInvoiceNo**: `int`
- **AmountReceivable**: `double`

## dTOPDReDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatientDataSets/_DsOPDRegister.cs)_
- **VisitDateTime**: `DateTime`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **Age**: `int`
- **Diagnosis**: `string`
- **Doctor**: `string`
- **VisitID**: `int`
- **HospitalName**: `string`
- **TotalBillAmount**: `float`
- **AgeMonths**: `int`
- **AgeWeeks**: `int`
- **Inscription**: `string`
- **Subscription**: `string`
- **Transcription**: `string`
- **Quantity**: `int`
- **QuantityPerTime**: `string`
- **FrequencyPerDay**: `string`
- **DosageDuration**: `string`
- **PeriodIn**: `string`
- **OtherInstruction**: `string`
- **DosageUnits**: `string`
- **Residence**: `string`
- **OutPatientNo**: `int`
- **DateOfBirth**: `DateTime`
- **IDNumber**: `string`
- **Telephone1**: `string`
- **IsReVisit**: `int`
- **NurseTriageID**: `int`
- **Temperature**: `string`
- **Weight**: `string`
- **BloodPressure**: `string`
- **Expr1**: `int`
- **TemperatureRemarks**: `string`
- **WeightRemarks**: `string`
- **BloodPressureRemarks**: `string`
- **RespirationRate**: `string`
- **RespirationRateRemarks**: `string`
- **PulseRate**: `string`
- **PulseRateRemarks**: `string`
- **Notes**: `string`

## dTObservationChartDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsObservationCharts.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **Telephone1**: `string`
- **AdmissionDateTime**: `DateTime`
- **DateTimePosted**: `DateTime`
- **AdmissionID**: `int`
- **Temperature**: `double`
- **Systolic**: `double`
- **Diastolic**: `double`
- **Pulse**: `double`
- **Respiratory**: `double`
- **SPo2**: `double`
- **Comments**: `string`
- **Username**: `string`

## dTOnAdmissionDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsOnAdmissionExamination.cs)_
- **Name**: `string`
- **LetterHead**: `string`
- **AdmissionDateTime**: `DateTime`
- **AdmissionID**: `int`
- **HeightOfFundus**: `string`
- **Presentation**: `string`
- **Enlargement**: `string`
- **Position**: `string`
- **Height**: `string`
- **Urine**: `string`
- **Genitals**: `string`
- **HB**: `string`
- **BP**: `string`
- **FetalHeart**: `string`
- **VaginalDischarge**: `string`
- **Weight**: `string`
- **Spleen**: `string`
- **Abnormalities**: `string`
- **TPR**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **Telephone1**: `string`
- **Sex**: `string`
- **Username**: `string`

## dTOpticalExaminationDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsOpticalExamination.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **MedReqOExamID**: `int`
- **VisitID**: `int`
- **DateTimeRequested**: `DateTime`
- **IsOutPatient**: `int`
- **IsSelfRequest**: `int`
- **Surname**: `string`
- **OutPatientNo**: `int`
- **OtherNames**: `string`
- **Age**: `int`
- **Sex**: `string`
- **TelephoneNo**: `string`
- **MedReqOExamItemID**: `int`
- **History**: `string`
- **OExaminationID**: `int`
- **TechniqueProcedure**: `string`
- **Findings**: `string`
- **Impression**: `string`
- **Comment**: `string`
- **RequestedBySysUID**: `int`
- **Examiner**: `string`
- **Center**: `string`
- **DateTimeDone**: `DateTime`
- **IsDone**: `int`
- **ReasonNotDone**: `string`
- **IsInternal**: `int`
- **Description**: `string`

## dTOpticalNotesDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsOpticalNotes.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **VisitDateTime**: `DateTime`
- **Age**: `int`
- **VisitID**: `int`
- **Histoy**: `string`
- **Examinations**: `string`
- **Diagnosis**: `string`
- **TreatmentPlan**: `string`
- **TreatmentDone**: `string`
- **DatePosted**: `DateTime`
- **DoctorID**: `int`
- **Expr1**: `string`
- **Registration**: `string`
- **DateTimeRequested**: `DateTime`
- **Expr2**: `int`
- **Sex**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **IDNumber**: `string`
- **OutPatientNo**: `int`
- **Telephone1**: `string`
- **GroupAccountID**: `int`
- **Expr3**: `string`

## dTOpticalsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsOpticals.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Age**: `int`
- **VisitDateTime**: `DateTime`
- **OpticalNotesID**: `int`
- **MedReqTestID**: `int`
- **Complaints**: `string`
- **Examinations**: `string`
- **Diagnosis**: `string`
- **Treatment**: `string`
- **DatePosted**: `DateTime`
- **Surname**: `string`
- **OtherNames**: `string`
- **Expr1**: `int`
- **Sex**: `string`
- **AgeMonths**: `int`
- **AgeWeeks**: `int`
- **VisitID**: `int`
- **PatientID**: `int`
- **Expr2**: `string`
- **Expr3**: `string`
- **Expr4**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **Telephone1**: `string`

## dTOrthopedicDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsOrthopedic.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Age**: `int`
- **AgeMonths**: `int`
- **AgeWeeks**: `int`
- **DateTimePosted**: `DateTime`
- **Notes**: `string`
- **Diagnosis**: `string`
- **Management**: `string`
- **Username**: `string`
- **PatientID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **OrthopedicID**: `uint`
- **VisitID**: `int`
- **NextOfKin**: `string`

## dTOutBillDetailedDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatBills/_DsOutPatientBillDetailed.cs)_
- **Name**: `string`
- **LetterHead**: `string`
- **MedicalBillID**: `int`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **AdvancePayment**: `float`
- **DateTimeCreated**: `DateTime`
- **IsProcessed**: `bool`
- **IsPatient**: `bool`
- **CustomerName**: `string`
- **CoverAmount**: `double`
- **Code**: `int`
- **Quantity**: `int`
- **Rate**: `double`
- **Amount**: `double`
- **DiscountedAmount**: `double`
- **Expr1**: `string`
- **CostAmount**: `double`
- **HasBeenPaidFor**: `int`
- **HasBeenDispensed**: `int`
- **GroupAccountID**: `int`
- **Expr2**: `string`

## dTOutPatBillsByDocDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatBills/_DsOutPatbillsByDoc.cs)_
- **IsProcessed**: `bool`
- **MedicalBillNo**: `int`
- **CoverAmount**: `double`
- **DepositOffset**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **DepositBalance**: `double`
- **Surname**: `string`
- **OtherNames**: `string`
- **GroupAccount**: `string`
- **HospitalName**: `string`
- **VisitID**: `int`
- **MedicalBillID**: `int`
- **OutPatientNo**: `int`
- **Doctor**: `string`
- **IsAdmitted**: `int`
- **DateTimeCreated**: `DateTime`
- **AdvancePayment**: `float`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`

## dTOutPatBillsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatBills/_DsOutPatBills.cs)_
- **DateTimeCreated**: `DateTime`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **IsProcessed**: `bool`
- **MedicalBillNo**: `int`
- **CoverAmount**: `double`
- **DepositOffset**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **DepositBalance**: `double`
- **Surname**: `string`
- **OtherNames**: `string`
- **GroupAccount**: `string`
- **HospitalName**: `string`
- **VisitID**: `int`
- **MedicalBillID**: `int`
- **AdmissionID**: `int`
- **OutPatientNo**: `int`
- **Doctor**: `string`
- **IsAdmitted**: `int`

## dTOutPatBillsDetailedDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatBills/_DsOutPatBillDetailed.cs)_
- **DateTimeCreated**: `DateTime`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **IsProcessed**: `bool`
- **MedicalBillNo**: `int`
- **CoverAmount**: `double`
- **DepositOffset**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **DepositBalance**: `double`
- **Surname**: `string`
- **OtherNames**: `string`
- **GroupAccount**: `string`
- **HospitalName**: `string`
- **VisitID**: `int`
- **MedicalBillID**: `int`
- **AdmissionID**: `int`
- **OutPatientNo**: `int`
- **Doctor**: `string`
- **CustomerName**: `string`
- **GroupAccountID**: `int`
- **LetterHead**: `string`

## dTOutPatByGrpAccountDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatBills/_DsOutPatVisitByGroupAccount.cs)_
- **VisitDateTime**: `DateTime`
- **Age**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **ThirdName**: `string`
- **PrincipalMember**: `string`
- **MembershipNo**: `string`
- **ARInvoiceNo**: `int`
- **TotalBillAmount**: `float`
- **GroupAccountID**: `int`
- **Name**: `string`
- **IsProcessed**: `bool`
- **Expr1**: `string`
- **LetterHead**: `string`

## dTOver5DataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.MOHDatasets/_Ds204Over5.cs)_
- **PatientID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **Residence**: `string`
- **OutPatientNo**: `int`
- **Telephone1**: `string`
- **Age**: `int`
- **VisitDateTime**: `DateTime`
- **Summary**: `string`
- **TotalBillAmount**: `float`
- **IsReferal**: `int`
- **IsFollowUp**: `int`
- **IllnessDuration**: `int`
- **MedicalSurgicalHistoryID**: `int`
- **PastMedicalHistory**: `string`
- **FamilySocioEconomicID**: `int`
- **PhysicalExam**: `string`
- **ComplaintID**: `int`
- **DiagnosisID**: `int`
- **Diagnosis**: `string`
- **Treatment**: `string`
- **Revisit**: `int`
- **Complaint**: `string`
- **InPatientNo**: `int`
- **IsAdmitted**: `int`

## dTOverCounterDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatBills/_DsOverCounterSales.cs)_
- **Name**: `string`
- **LetterHead**: `string`
- **MedicalBillID**: `int`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **AdvancePayment**: `float`
- **DateTimeCreated**: `DateTime`
- **IsProcessed**: `bool`
- **IsPatient**: `bool`
- **CustomerName**: `string`
- **CoverAmount**: `double`
- **Code**: `int`
- **Quantity**: `int`
- **Rate**: `double`
- **Amount**: `double`
- **DiscountedAmount**: `double`
- **Expr1**: `string`
- **CostAmount**: `double`

## dTPOsGRNsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.ProcurementDatasets/_DsPOsGRNs.cs)_
- **PurchaseOrderNo**: `int`
- **HasBeenReceived**: `int`
- **HospitalName**: `string`
- **DateTimeCreatedGRN**: `DateTime`
- **TotalNetAmount**: `double`
- **TotalAmountPaid**: `double`
- **APInvoiceNo**: `string`
- **TotalCreditNoteAmount**: `double`
- **GRNID**: `int`
- **SupplierName**: `string`
- **IsCommittedToStockGRN**: `int`
- **SupplierID**: `int`
- **LetterHead**: `string`

## dTPTListPerGrpAccountDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatientDataSets/_DsPatientListPerGrpAccount.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **Telephone1**: `string`
- **ThirdName**: `string`
- **GroupAccountID**: `int`
- **Expr1**: `string`
- **DateRegistered**: `DateTime`

## dTPatDetailDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsMedicalBillInPatient.cs)_
- **Age**: `int`
- **Doctor**: `string`
- **DateTimeCreated**: `DateTime`
- **AdvancePayment**: `float`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **MedicalBillNo**: `int`
- **CustomerName**: `string`
- **CoverAmount**: `double`
- **DepositOffset**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **Surname**: `string`
- **OtherNames**: `string`
- **DepositBalance**: `double`
- **Expr1**: `string`
- **Expr2**: `string`
- **Sex**: `string`
- **Residence**: `string`
- **IDNumber**: `string`
- **OutPatientNo**: `int`
- **Telephone1**: `string`

## dTPatDetailsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsMedicalBill.cs)_
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **Residence**: `string`
- **PostalAddress**: `string`
- **CityTown**: `string`
- **OutPatientNo**: `int`
- **Telephone1**: `string`
- **PostalCode**: `string`
- **PatientID**: `int`
- **Age**: `int`
- **VisitID**: `int`
- **VisitDateTime**: `DateTime`
- **InPatientNo**: `int`

## dTPatientByDocDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatBills/_DsOutPatientBillsByDoc.cs)_
- **DateTimeCreated**: `DateTime`
- **TotalBillAmount**: `float`
- **TotalAmountPaid**: `float`
- **IsProcessed**: `bool`
- **MedicalBillNo**: `int`
- **CoverAmount**: `double`
- **DepositOffset**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **DepositBalance**: `double`
- **Surname**: `string`
- **OtherNames**: `string`
- **GroupAccount**: `string`
- **HospitalName**: `string`
- **VisitID**: `int`
- **MedicalBillID**: `int`
- **AdmissionID**: `int`
- **OutPatientNo**: `int`
- **Doctor**: `string`

## dTPatientDetailsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.MOHDatasets/_Ds204AUnder5.cs)_
- **PatientID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **Residence**: `string`
- **OutPatientNo**: `int`
- **Telephone1**: `string`
- **Age**: `int`
- **VisitDateTime**: `DateTime`
- **Summary**: `string`
- **TotalBillAmount**: `float`
- **IsReferal**: `int`
- **IsFollowUp**: `int`
- **IllnessDuration**: `int`
- **Description**: `string`
- **MedicalSurgicalHistoryID**: `int`
- **ComplaintID**: `int`
- **DiagnosisID**: `int`
- **FamilySocioEconomicID**: `int`
- **PastMedicalHistory**: `string`
- **PhysicalExam**: `string`
- **Diagnosis**: `string`
- **Expr1**: `int`
- **Treatment**: `string`
- **IsAdmitted**: `int`
- **IllnessDuration1**: `string`

## dTPatientGrpAccDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsBillsFilteredByGrpAccount.cs)_
- **Surname**: `string`
- **OtherNames**: `string`
- **OutPatientNo**: `int`
- **VisitDateTime**: `DateTime`
- **DateTimeCreated**: `DateTime`
- **VisitID**: `int`
- **MedicalBillNo**: `int`
- **GroupAccountName**: `string`
- **HospitalName**: `string`
- **LetterHead**: `string`
- **MedicalBillID**: `int`
- **Balance**: `double`
- **TotalAmountPaid**: `double`
- **TotalBillAmount**: `double`

## dTPatientHistoryDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPatientHistory.cs)_
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **Residence**: `string`
- **PostalAddress**: `string`
- **CityTown**: `string`
- **EmailAddress**: `string`
- **OutPatientNo**: `int`
- **Telephone1**: `string`
- **PostalCode**: `string`
- **HospitalName**: `string`
- **LetterHead**: `string`

## dTPatientInfoDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPatientVisit.cs)_
- **HospitalName**: `string`
- **LetterHead**: `string`
- **VisitID**: `int`
- **Age**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **Occupation**: `string`
- **Residence**: `string`
- **PostalAddress**: `string`
- **EmailAddress**: `string`
- **Telephone1**: `string`
- **OutPatientNo**: `int`
- **PostalCode**: `string`
- **CityTown**: `string`
- **Summary**: `string`
- **VisitDateTime**: `DateTime`
- **Doctor**: `string`
- **HPI**: `string`
- **AgeMonths**: `int`
- **AgeWeeks**: `int`
- **Nurse**: `string`

## dTPatientLabTestsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.Lab/_DsPatientLabTests.cs)_
- **Value**: `string`
- **VisitID**: `int`
- **Age**: `int`
- **Units**: `string`
- **TestControl**: `string`
- **TestComponent**: `string`
- **HospitalName**: `string`
- **LetterHead**: `string`
- **Specimen**: `string`
- **Test**: `string`
- **DateTimeDone**: `DateTime`
- **Remark**: `string`
- **Technologist**: `string`
- **DateTimeRequested**: `DateTime`
- **OtherNames**: `string`
- **Sex**: `string`
- **IsSelfRequest**: `int`
- **OutPatientNo**: `int`
- **RequestedBy**: `string`
- **Conclusion**: `string`
- **NormalRange**: `string`
- **AgeMonths**: `int`
- **AgeWeeks**: `int`
- **Surname**: `string`
- **Telephone1**: `string`
- **Residence**: `string`
- **CityTown**: `string`
- **TestDoneDate**: `DateTime`

## dTPatientRegDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatientDataSets/_DsPatientsReg.cs)_
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Occupation**: `string`
- **Residence**: `string`
- **PostalAddress**: `string`
- **CityTown**: `string`
- **NextOfKin**: `string`
- **NextOfKinRelationship**: `string`
- **NextOfKinContact**: `string`
- **EmailAddress**: `string`
- **DateRegistered**: `DateTime`
- **IDTypeID**: `int`
- **IDNumber**: `string`
- **OutPatientNo**: `int`
- **InPatientNo**: `int`
- **Telephone1**: `string`
- **Telephone2**: `string`
- **PostalCode**: `string`
- **Note**: `string`
- **GroupAccountID**: `int`
- **ReferenceNo**: `string`
- **NationalityID**: `int`
- **Nationality**: `string`
- **IDType**: `string`
- **GroupAccount**: `string`
- **PatientID**: `int`
- **RegisteredBy**: `string`

## dTPatientTemperatureDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.InPatientDataSets/_DsPatientTemperature.cs)_
- **Name**: `string`
- **LetterHead**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **DateOfBirth**: `DateTime`
- **OutPatientNO**: `int`
- **InPatientNo**: `int`
- **Value**: `string`
- **TempDateTimeDone**: `DateTime`

## dTPatientsVisitsRegisterDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPatientVisitsRegister.cs)_
- **VisitDateTime**: `DateTime`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **Age**: `int`
- **Diagnosis**: `string`
- **Doctor**: `string`
- **VisitID**: `int`
- **HospitalName**: `string`
- **TotalBillAmount**: `float`
- **AgeMonths**: `int`
- **AgeWeeks**: `int`
- **ClinicID**: `int`
- **Name**: `string`
- **Summary**: `string`
- **HPI**: `string`
- **IsAdmitted**: `int`

## dTPaymentDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsMedicalBillInPatient.cs)_
- **IssuedByUserName**: `string`
- **IssuedReceiptNo**: `int`
- **DateTimeIssued**: `DateTime`
- **AmountPaid**: `double`
- **PaymentMode**: `string`
- **MedicalBillID**: `int`
- **PaidInBy**: `string`
- **IsCustomerDeposit**: `int`
- **HasBeenCancelled**: `int`

## dTPaymentVoucherDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsPaymentVoucher.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **SupplierBillNo**: `uint`
- **DateTimeDue**: `DateTime`
- **Terms**: `string`
- **ReferenceNo**: `string`
- **APInvoiceNo**: `string`
- **TotalNetAmount**: `double`
- **TotalCreditNoteAmount**: `double`
- **IsSettled**: `bool`
- **TotalAmountPaid**: `double`
- **DateTimeCreated**: `DateTime`
- **IsApproved**: `int`
- **DateTimeApproved**: `DateTime`
- **SupplierID**: `int`
- **SupplierName**: `string`
- **Telephone1**: `string`
- **SystemUserID**: `int`
- **Username**: `string`
- **SupplierBillID**: `int`

## dTPaymentsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsMedicalBillPayments.cs)_
- **PaidInBy**: `string`
- **DateTimePaid**: `DateTime`
- **IssuedReceiptNo**: `int`
- **AmountPaid**: `double`

## dTPayrollParamDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.HRDatasets/_DsPayrollParam.cs)_
- **HospitalName**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **PayrollNo**: `string`
- **NSSFNo**: `string`
- **NHIFNo**: `string`
- **PINNo**: `string`
- **IDNo**: `string`
- **StaffNo**: `string`
- **PayslipPeriodID**: `int`
- **PayYear**: `int`
- **BeginningDateTime**: `DateTime`
- **EndingDateTime**: `DateTime`
- **PayMonth**: `string`
- **EmployeePayslipParameterID**: `int`
- **PayrollParameterName**: `string`
- **ParameterCategoryType**: `string`
- **ParameterCategoryName**: `string`
- **Amount**: `double`
- **PayrollParameterID**: `int`

## dTPayslipDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.HRDatasets/_DsPayslip.cs)_
- **Surname**: `string`
- **OtherNames**: `string`
- **StaffNo**: `string`
- **IDNo**: `string`
- **PINNo**: `string`
- **BasicPayTotal**: `double`
- **OvertimeTotal**: `double`
- **HousingAllowanceTotal**: `double`
- **ElectricityAllowanceTotal**: `double`
- **CommuterAllowanceTotal**: `double`
- **OverTaxationTotal**: `double`
- **UnderPaymentTotal**: `double`
- **OtherAllowanceTotal**: `double`
- **PAYETotal**: `double`
- **FringeBenefitTaxTotal**: `double`
- **NSSFTotal**: `double`
- **NHIFTotal**: `double`
- **LoanRepaymentTotal**: `double`
- **SalaryAdvanceRecoveryTotal**: `double`
- **OtherPensionTotal**: `double`
- **EmployerContributionTotal**: `double`
- **NetPay**: `double`
- **BeginningDateTime**: `DateTime`
- **EndingDateTime**: `DateTime`
- **PayYear**: `int`
- **PayMonth**: `string`
- **PayslipID**: `int`
- **PaymentModeID**: `int`
- **OtherDeductionTotal**: `double`
- **LeaveAllowanceTotal**: `double`
- **IsPaid**: `int`
- **NHIFNo**: `string`
- **NSSFNo**: `string`
- **PayrollNo**: `string`
- **PaymentMode**: `string`
- **HospitalName**: `string`
- **GrossEarningTotal**: `double`
- **GrossTaxablePayTotal**: `double`
- **NSSFReliefTotal**: `double`
- **OtherPensionReliefTotal**: `double`
- **TaxableAmountTotal**: `double`
- **TaxChargeableTotal**: `double`
- **PersonalReliefTotal**: `double`
- **DeductionTotal**: `double`
- **BankAccountNo**: `string`
- **Department**: `string`
- **Designation**: `string`
- **SaccoTotal**: `double`
- **BankName**: `string`
- **BranchCode**: `string`
- **BankBranch**: `string`

## dTPayslipsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.HRDatasets/_DsPayslips.cs)_
- **HospitalName**: `string`
- **EmployeeID**: `int`
- **StaffNo**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **PINNo**: `string`
- **DateEmployed**: `DateTime`
- **Telephone1**: `string`
- **NHIFNo**: `string`
- **NSSFNo**: `string`
- **Department**: `string`
- **PayYear**: `int`
- **PayMonth**: `string`
- **BasicPayTotal**: `double`
- **OvertimeTotal**: `double`
- **HousingAllowanceTotal**: `double`
- **ElectricityAllowanceTotal**: `double`
- **CommuterAllowanceTotal**: `double`
- **LeaveAllowanceTotal**: `double`
- **OverTaxationTotal**: `double`
- **UnderPaymentTotal**: `double`
- **OtherAllowanceTotal**: `double`
- **GrossEarningTotal**: `double`
- **GrossTaxablePayTotal**: `double`
- **NSSFReliefTotal**: `double`
- **OtherPensionReliefTotal**: `double`
- **PAYETotal**: `double`
- **FringeBenefitTaxTotal**: `double`
- **NSSFTotal**: `double`
- **NHIFTotal**: `double`
- **LoanRepaymentTotal**: `double`
- **SalaryAdvanceRecoveryTotal**: `double`
- **OtherPensionTotal**: `double`
- **OtherDeductionTotal**: `double`
- **EmployerContributionTotal**: `double`
- **TaxableAmountTotal**: `double`
- **TaxChargeableTotal**: `double`
- **PersonalReliefTotal**: `double`
- **DeductionTotal**: `double`
- **NetPay**: `double`
- **PayslipPeriodID**: `int`
- **PayslipID**: `int`
- **BranchCode**: `string`
- **BankName**: `string`
- **BankCode**: `string`
- **EmploymentType**: `string`

## dTPhysioRequestDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPhysioResults.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Age**: `int`
- **AgeMonths**: `int`
- **AgeWeeks**: `int`
- **VisitID**: `int`
- **Complaints**: `string`
- **Examinations**: `string`
- **Diagnosis**: `string`
- **Treatment**: `string`
- **DatePosted**: `DateTime`
- **Username**: `string`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **Residence**: `string`
- **Telephone1**: `string`
- **IsOrthopaedic**: `int`
- **IsPhysio**: `int`
- **IsOptical**: `int`

## dTPresDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPres.cs)_
- **Description**: `string`
- **SpecialInstruction**: `string`
- **PrescriptionNo**: `int`
- **VisitID**: `int`
- **Inscription**: `string`
- **Subscription**: `string`
- **Transcription**: `string`
- **Quantity**: `int`
- **QuantityPerTime**: `string`
- **FrequencyPerDay**: `string`
- **DosageDuration**: `string`
- **PeriodIn**: `string`
- **OtherInstruction**: `string`
- **DosageUnits**: `string`

## dTPresInfoDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPres.cs)_
- **VisitDateTime**: `DateTime`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **Residence**: `string`
- **EmailAddress**: `string`
- **Telephone1**: `string`
- **VisitID**: `int`
- **LetterHead**: `string`
- **HospitalName**: `string`
- **OutPatientNo**: `int`
- **Age**: `int`
- **Nurse**: `string`
- **Doctor**: `string`
- **AgeMonths**: `int`
- **AgeWeeks**: `int`

## dTPrescriptionDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPatientVisit.cs)_
- **VisitID**: `int`
- **Description**: `string`
- **PrescriptionNo**: `int`
- **Inscription**: `string`
- **Subscription**: `string`
- **Transcription**: `string`
- **Quantity**: `int`
- **QuantityPerTime**: `string`
- **FrequencyPerDay**: `string`
- **DosageDuration**: `string`
- **PeriodIn**: `string`
- **OtherInstruction**: `string`
- **DosageUnits**: `string`
- **SpecialInstruction**: `string`
- **PrescriptionItemID**: `int`

## dTProcessByDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsMedicalBillInPatient.cs)_
- **Username**: `string`
- **MedicalBillID**: `int`
- **DateTimeProcessed**: `string`
- **ARInvoiceID**: `int`

## dTProcessedByUserDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsMedicalBill.cs)_
- **Username**: `string`
- **MedicalBillID**: `int`
- **DateTimeProcessed**: `string`

## dTPurchaseOrderDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPurchaseOrder.cs)_
- **PurchaseOrderNo**: `int`
- **Validitydate**: `DateTime`
- **DeliveryNoteNo**: `string`
- **OrderNo**: `string`
- **TermsConditions**: `string`
- **Name**: `string`
- **Description**: `string`
- **Quality**: `string`
- **Quantity**: `int`
- **Rate**: `double`
- **Amount**: `double`
- **PercentageDiscount**: `double`
- **DiscountedAmount**: `double`
- **UnitDefination**: `string`
- **HospitalName**: `string`
- **LetterHead**: `string`
- **ContactPerson**: `string`
- **PhysicalAddress**: `string`
- **PostalAddress**: `string`
- **PostalCode**: `string`
- **TownCity**: `string`
- **Country**: `string`
- **Telephone1**: `string`
- **Telephone2**: `string`
- **EmailAddress**: `string`
- **WebAddress**: `string`
- **SupplierName**: `string`
- **supplierDescription**: `string`
- **DateTimeIssued**: `DateTime`
- **PreparedByID**: `int`
- **CheckedByID**: `int`
- **DateTimeReceived**: `DateTime`
- **ReceivedByID**: `int`
- **InvoiceNo**: `string`
- **HasBeenReceived**: `int`
- **HasBeenChecked**: `int`
- **DateTimeChecked**: `DateTime`
- **OrderReference**: `string`
- **PercentageVAT**: `double`

## dTPurchaseOrdersDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPurchaseOrders.cs)_
- **PurchaseOrderNo**: `int`
- **Validitydate**: `DateTime`
- **DeliveryNoteNo**: `string`
- **OrderNo**: `string`
- **CommittedToStock**: `string`
- **HospitalName**: `string`
- **LetterHead**: `string`
- **SumOfDiscountedAmount**: `double`
- **SupplierName**: `string`
- **DateTimeIssued**: `DateTime`
- **PreparedByID**: `int`
- **CheckedByID**: `int`
- **DateTimeReceived**: `DateTime`
- **ReceivedByID**: `int`
- **InvoiceNo**: `string`
- **HasBeenReceived**: `int`
- **LetterHead1**: `string`

## dTQueueDataTableDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.QueueDatasets/_DsQueue.cs)_
- **QueueID**: `int`
- **QueueItemID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **OutPatientNo**: `int`
- **FromRoom**: `string`
- **ToRoom**: `string`
- **WaitingTime**: `int`
- **ServiceTime**: `int`
- **TotalTime**: `int`
- **QueueDateTimeIn**: `DateTime`
- **QueueDateTimeOut**: `DateTime`
- **RoomDateTimeIn**: `DateTime`
- **RoomDateTimeOut**: `DateTime`
- **HospitalName**: `string`
- **DateTimeCreated**: `DateTime`

## dTReceiptRefundDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatBills/_DsReceiptsRefunds.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **IssuedReceiptNo**: `int`
- **DateTimeIssued**: `DateTime`
- **RefundAmount**: `double`
- **Reason**: `string`
- **DateTimePosted**: `DateTime`
- **IssuedTo**: `string`
- **AmountReceived**: `double`
- **Username**: `string`

## dTReferalFormDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsReferalForm.cs)_
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **ClinicalNotes**: `string`
- **Diagnosis**: `string`
- **Investigations**: `string`
- **Treatments**: `string`
- **ToDoctor**: `string`
- **ReferedReason**: `string`
- **ToHospital**: `string`
- **ReferedBy**: `string`
- **DateTimeReferred**: `DateTime`
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **referalformID**: `int`
- **IDNumber**: `string`
- **Telephone1**: `string`
- **MembershipNo**: `string`
- **CompanyName**: `string`

## dTReqStorageLocDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.ProcurementDatasets/_DsInternalOrder.cs)_
- **InternalOrderID**: `int`
- **RequestingStorageLocationID**: `int`
- **ApprovedBy**: `string`
- **RequestingLocation**: `string`

## dTSExaminationsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPatientVisit.cs)_
- **Remark**: `string`
- **Description**: `string`

## dTSalaryDisbDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.HRDatasets/_DsSalaryDisb.cs)_
- **Surname**: `string`
- **OtherNames**: `string`
- **IDNo**: `string`
- **PINNo**: `string`
- **BankName**: `string`
- **StaffNo**: `string`
- **PayrollNo**: `string`
- **BankAccountNo**: `string`
- **NetPay**: `double`
- **IsPaid**: `int`
- **PayslipPeriodID**: `int`
- **BeginningDateTime**: `DateTime`
- **EndingDateTime**: `DateTime`
- **PayYear**: `int`
- **PayMonth**: `string`
- **BankID**: `int`
- **PayslipID**: `int`
- **HospitalName**: `string`
- **IDType**: `string`

## dTSaleItemDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsMedicalBillInPatient.cs)_
- **Code**: `int`
- **Quantity**: `int`
- **Rate**: `double`
- **PercentageDiscount**: `double`
- **Amount**: `double`
- **DiscountedAmount**: `double`
- **DateTimeSold**: `DateTime`
- **Name**: `string`
- **Description**: `string`
- **MedicalBillID**: `int`
- **SaleItemID**: `int`
- **VAT**: `double`
- **CategoryName**: `string`
- **ConsultantAlias**: `string`

## dTSaleItemsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsSaleItems.cs)_
- **MedicalBillID**: `int`
- **Code**: `int`
- **Quantity**: `int`
- **Rate**: `double`
- **PercentageDiscount**: `double`
- **DiscountedAmount**: `double`
- **Name**: `string`
- **SaleItemID**: `int`
- **IssuedReceiptID**: `int`
- **VAT**: `double`
- **Amount**: `double`
- **DateTimeSold**: `DateTime`
- **Description**: `string`
- **CategoryName**: `string`
- **ConsultantAlias**: `string`
- **HasBeenPaidFor**: `int`
- **IsCashSale**: `int`
- **CostAmount**: `double`
- **VATAmount**: `double`
- **CoverAmount**: `double`
- **DepositOffset**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **DepositBalance**: `double`
- **IsPatient**: `bool`
- **HospitalInfoID**: `int`
- **SaleItemName**: `string`

## dTSaleItemsServicesDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsSaleItemsServices.cs)_
- **CoverAmount**: `double`
- **DepositOffset**: `double`
- **SalesDiscountAmount**: `double`
- **WriteOffAmount**: `double`
- **DepositBalance**: `double`
- **IsPatient**: `bool`
- **HospitalInfoID**: `int`
- **Name**: `string`
- **SaleItemID**: `int`
- **Code**: `int`
- **Quantity**: `int`
- **Rate**: `double`
- **PercentageDiscount**: `double`
- **Amount**: `double`
- **DiscountedAmount**: `double`
- **DateTimeSold**: `DateTime`
- **SaleItemName**: `string`
- **CostAmount**: `double`
- **VAT**: `double`
- **VATAmount**: `double`
- **HasBeenPaidFor**: `int`
- **IsCashSale**: `int`

## dTSalesDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsSales.cs)_
- **MedicalBillNo**: `int`
- **Code**: `int`
- **Quantity**: `int`
- **Rate**: `double`
- **PercentageDiscount**: `double`
- **Amount**: `double`
- **DiscountedAmount**: `double`
- **DateTimeSold**: `DateTime`
- **Name**: `string`
- **Description**: `string`
- **LetterHead**: `string`
- **HospitalName**: `string`
- **CostAmount**: `double`
- **ItemCategoryName**: `string`
- **VATAmount**: `double`
- **IsCashSale**: `int`
- **Department**: `string`
- **IssuedReceiptNo**: `int`
- **DateTimeIssued**: `DateTime`
- **StorageLocationID**: `int`
- **SystemUserID**: `int`
- **ItemCategoryID**: `int`
- **DepartmentID**: `int`
- **HasBeenPaidFor**: `int`

## dTSalesOrderDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsSalesOrder.cs)_
- **CustomerName**: `string`
- **DateTimeCreated**: `DateTime`
- **SalesOrderID**: `int`
- **ItemName**: `string`
- **QuantityOrdered**: `int`
- **Rate**: `double`
- **NetAmount**: `double`
- **Amount**: `double`
- **HospitalName**: `string`
- **IsProcessed**: `int`
- **StorageLocationID**: `int`
- **ItemCategoryID**: `int`
- **DepartmentID**: `int`
- **Code**: `int`
- **PercentageVAT**: `double`
- **PercentageDiscount**: `double`
- **SalesOrderItemID**: `int`

## dTServiceProductCostDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsServiceProductCost.cs)_
- **MedicalBillNo**: `int`
- **DateTimeCreated**: `DateTime`
- **ServiceName**: `string`
- **ProductName**: `string`
- **RequiredQuantity**: `double`
- **MaterialCost**: `double`
- **HospitalName**: `string`
- **LetterHead**: `string`
- **RequiredQuantityUnits**: `string`

## dTServiceRequestDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsServiceRequests.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **MedicalBillID**: `int`
- **DateTimeCreated**: `DateTime`
- **CustomerName**: `string`
- **Age**: `int`
- **SaleItemID**: `int`
- **Quantity**: `int`
- **Rate**: `double`
- **DateTimeSold**: `DateTime`
- **ItemName**: `string`
- **HasBeenPaidFor**: `int`
- **IsCashSale**: `int`
- **HasBeenDispensed**: `int`
- **SystemUserID**: `int`
- **Username**: `string`
- **PatientID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **IDNumber**: `string`
- **Telephone1**: `string`
- **ThirdName**: `string`
- **GroupAccountID**: `int`
- **groupAccount**: `string`
- **Code**: `int`

## dTSettingsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsReceipt.cs)_
- **ReceiptAdvert**: `string`
- **SettingName**: `string`

## dTShiftINvoicesDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsShiftARInvoices.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **ARInvoiceNo**: `int`
- **DateTimeCreated**: `DateTime`
- **AmountReceivable**: `double`
- **InvoiceTo**: `string`
- **PreparedBy**: `string`
- **CoverAmount**: `double`
- **ShiftID**: `int`
- **DateTimePosted**: `DateTime`

## dTSickSheetDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsSickSheet.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **SickSheetID**: `int`
- **VisitID**: `int`
- **Reason**: `string`
- **Recomendation**: `string`
- **StartDate**: `DateTime`
- **EndDateTime**: `DateTime`
- **Duration**: `string`
- **DateTimePosted**: `DateTime`
- **PatientID**: `int`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **IDNumber**: `string`
- **OutPatientNo**: `int`
- **Telephone1**: `string`
- **ThirdName**: `string`
- **Username**: `string`

## dTStockAllDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.ProcurementDatasets/_DsStockAll.cs)_
- **Name**: `string`
- **UnitCost**: `float`
- **UnitPrice**: `float`
- **UnitDefination**: `string`
- **PackedQuantity**: `float`
- **Quantity**: `int`
- **UnitCost1**: `double`
- **UnitPrice1**: `double`
- **ProductID**: `int`
- **ReorderLevel**: `int`
- **EarliestExpiryDate**: `DateTime`
- **StorageLocationID**: `int`
- **Expr1**: `string`
- **HospitalInfoID**: `int`
- **Expr2**: `string`
- **LetterHead**: `string`

## dTStockDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsStockExpiry.cs)_
- **Name**: `string`
- **UnitCost**: `double`
- **UnitPrice**: `double`
- **LetterHead**: `string`
- **ProductID**: `int`
- **Quantity**: `int`
- **ReorderLevel**: `int`
- **EarliestExpiryDate**: `DateTime`
- **Code**: `int`
- **Description**: `string`
- **UnitDefination**: `string`
- **Quality**: `string`
- **HospitalName**: `string`
- **LetterHead1**: `string`
- **StorageLocation**: `string`
- **Expr1**: `string`
- **StorageLocationID**: `int`
- **BatchNo**: `string`

## dTStockListDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsStockList.cs)_
- **ProductID**: `int`
- **Code**: `int`
- **Name**: `string`
- **Description**: `string`
- **UnitCost**: `double`
- **UnitPrice**: `double`
- **UnitDefination**: `string`
- **Quality**: `string`
- **PackedQuantityUnit**: `string`
- **PackedQuantity**: `double`
- **HospitalInfoID**: `int`
- **Name1**: `string`
- **BuildingName**: `string`
- **StreetName**: `string`
- **PostalAddress**: `string`
- **TownCity**: `string`
- **PostalCode**: `string`
- **Telephone1**: `string`
- **Telephone2**: `string`
- **Telephone3**: `string`
- **FaxNo**: `string`
- **EmailAddress**: `string`
- **Website**: `string`
- **RegistrationNo**: `string`
- **KRAPINNo**: `string`
- **KRAVATNo**: `string`
- **KRAAgentNo**: `string`
- **LetterHead**: `string`
- **CustomerKey**: `string`
- **Min**: `string`
- **Max**: `string`
- **LicenseStatus**: `string`
- **ProductStorageLocationID**: `int`
- **StorageLocationID**: `int`
- **ProductID1**: `int`
- **Quantity**: `int`
- **TotalPackedQuantity**: `int`
- **ReorderLevel**: `int`
- **EarliestExpiryDate**: `DateTime`
- **ItemCategoryID**: `int`
- **DepartmentID**: `int`
- **StorageLocationID1**: `int`
- **Name2**: `string`
- **Description1**: `string`
- **IsDefaultSellPoint**: `int`

## dTStockListPerLocationDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsStocklistPerLocation.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Quantity**: `int`
- **ReorderLevel**: `int`
- **EarliestExpiryDate**: `DateTime`
- **ProductID**: `int`
- **ItemName**: `string`
- **UnitCost**: `double`
- **UnitPrice**: `double`
- **NationalScheme**: `double`
- **StorageLocationID**: `int`
- **Storagelocation**: `string`
- **EduAfya**: `double`
- **NHIFNPS**: `double`
- **MaklTSC2021**: `double`
- **NHIFFFS**: `double`
- **MaklG4SPamoja**: `double`
- **MaklServiceProvider**: `double`
- **MaklKWFTAfyaFit**: `double`
- **MinetFamilyBank**: `double`
- **MinetSafaricom**: `double`
- **MinetNSSF**: `double`
- **SahamMua**: `double`
- **KCB**: `double`
- **Jubilee**: `double`
- **AAR**: `double`
- **Mtiba**: `double`
- **Resolution**: `double`
- **Liason**: `double`

## dTStockValuationLocationDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.ProcurementDatasets/_DsStockAllPerLocation.cs)_
- **ProductID**: `int`
- **Name**: `string`
- **UnitCost**: `double`
- **UnitPrice**: `double`
- **UnitDefination**: `string`
- **Quantity**: `int`
- **ReorderLevel**: `int`
- **EarliestExpiryDate**: `DateTime`
- **StorageLocationID**: `int`
- **StorageLocation**: `string`
- **HospitalInfoID**: `int`
- **CompanyName**: `string`
- **LetterHead**: `string`

## dTStorageStockListDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsStorageStockList.cs)_
- **StorageLocation**: `string`
- **Name**: `string`
- **UnitCost**: `double`
- **Quantity**: `int`
- **ReorderLevel**: `int`
- **Expr1**: `string`
- **LetterHead**: `string`

## dTSubAccountHistoryDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsSubAccountHistory.cs)_
- **HospitalName**: `string`
- **LetterHead**: `string`
- **SubAccountName**: `string`
- **SourceReference**: `string`
- **Description**: `string`
- **TransactionAmount**: `double`
- **Username**: `string`
- **AmountPosted**: `double`
- **TransactionDateTime**: `DateTime`
- **AccountName**: `string`
- **JournalVoucherID**: `int`
- **EntryType**: `int`
- **AccountType**: `string`
- **NetBalance**: `double`
- **AccountTypeName**: `string`
- **FiscalPeriodID**: `int`

## dTSuppBillDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsSupplierBillsSummary.cs)_
- **SupplierBillNo**: `uint`
- **SupplierName**: `string`
- **HospitalName**: `string`
- **TotalNetAmount**: `double`
- **TotalAmountPaid**: `double`
- **CreatedBy**: `string`
- **TransactionDateTime**: `DateTime`
- **DateTimeDue**: `DateTime`
- **APInvoiceNo**: `string`
- **IsSettled**: `bool`
- **TotalCreditNoteAmount**: `double`

## dTSuppBillPaymentDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsSuppBillsPaySummary.cs)_
- **SupplierBillNo**: `uint`
- **SupplierName**: `string`
- **TotalNetAmount**: `double`
- **HospitalName**: `string`
- **PaymentModeID**: `int`
- **PaymentDateTime**: `DateTime`
- **PaidOutBy**: `string`
- **SupplierID**: `int`
- **ChequeNo**: `string`
- **PettyCashVoucherNo**: `string`
- **ReferenceNo**: `string`
- **DateTimeDue**: `DateTime`
- **APInvoiceNo**: `string`
- **SupplierBillPaymentAmount**: `double`
- **TotalAmountPaid**: `double`

## dTSupplierBillInvoiceDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsSupplierBillInvoice.cs)_
- **SupplierName**: `string`
- **PhysicalAddress**: `string`
- **TownCity**: `string`
- **Country**: `string`
- **Telephone1**: `string`
- **Telephone2**: `string`
- **EmailAddress**: `string`
- **WebAddress**: `string`
- **SupplierBillNo**: `uint`
- **Terms**: `string`
- **ReferenceNo**: `string`
- **APInvoiceNo**: `string`
- **IsSettled**: `bool`
- **TotalNetAmount**: `double`
- **TotalCreditNoteAmount**: `double`
- **TotalAmountPaid**: `double`
- **HospitalInfo**: `string`
- **PurchaseOrderNo**: `int`
- **Item**: `string`
- **UnitOfMeasure**: `string`
- **Quantity**: `int`
- **UnitCost**: `double`
- **PercentageVAT**: `double`
- **Amount**: `double`
- **PercentageDiscount**: `double`
- **NetAmount**: `double`
- **SupplierBillID**: `int`
- **DateTimeDue**: `DateTime`

## dTTBScreenDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsTBScreening.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **Age**: `int`
- **VisitDateTime**: `DateTime`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **ThirdName**: `string`
- **IsUnder5**: `int`
- **IsCough**: `int`
- **IsLossWeight**: `int`
- **IsNightSweats**: `int`
- **IsFever**: `int`
- **IsReducedPlay**: `int`
- **Doctor**: `string`
- **TBScreeningID**: `int`
- **IsPositive**: `int`

## dTTheatreListDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsTheatreList.cs)_
- **DateTimePosted**: `DateTime`
- **IsDone**: `int`
- **Operation**: `string`
- **Name**: `string`
- **LetterHead**: `string`
- **AdmissionDateTime**: `DateTime`
- **Surname**: `string`
- **OtherNames**: `string`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Telephone1**: `string`

## dTTrackSaleItemDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsTrackSaleItem.cs)_
- **HospitalInfoID**: `int`
- **Name**: `string`
- **GroupAccountID**: `int`
- **SaleItemID**: `int`
- **Code**: `int`
- **Quantity**: `int`
- **Rate**: `double`
- **PercentageDiscount**: `double`
- **DiscountedAmount**: `double`
- **DateTimeSold**: `DateTime`
- **ItemName**: `string`
- **CostAmount**: `double`
- **HasBeenPaidFor**: `int`
- **IsCashSale**: `int`
- **Expr1**: `string`
- **Username**: `string`

## dTTrialBalanceDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsTrialBalance.cs)_
- **NetBalance**: `double`
- **SubAccountName**: `string`
- **MainAccountName**: `string`
- **AccountTypeName**: `string`
- **HospitalName**: `string`
- **LetterHead**: `string`
- **AccountNo**: `int`
- **FromDateTime**: `DateTime`
- **ToDateTime**: `DateTime`

## dTVirtualInvoiceDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsVirtualInvoice.cs)_
- **ARInvoiceNo**: `int`
- **IDNumber**: `string`
- **PhoneNumber**: `string`
- **Name**: `string`
- **VirtualInvoiceID**: `int`
- **DateTimePosted**: `DateTime`
- **InvoiceName**: `string`
- **InvoiceAddress**: `string`
- **TotalAmount**: `double`
- **HospitalInfoID**: `int`
- **ComapnyName**: `string`
- **LetterHead**: `string`
- **SaleItemID**: `int`
- **ItemName**: `string`
- **Quantity**: `int`
- **Code**: `int`
- **Rate**: `double`
- **PercentageDiscount**: `double`
- **Amount**: `double`
- **DiscountedAmount**: `double`
- **DateTimeSold**: `DateTime`
- **VAT**: `double`
- **VATAmount**: `double`
- **Username**: `string`
- **OrderNo**: `string`
- **MemberNo**: `string`
- **OPDNo**: `string`

## dtPresItemDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets/_DsPrescriptionSaleItems.cs)_
- **MedicalBillID**: `int`
- **VisitID**: `int`
- **DateTimeCreated**: `DateTime`
- **CustomerName**: `string`
- **Code**: `int`
- **Expr1**: `int`
- **Quantity**: `int`
- **Rate**: `double`
- **Amount**: `double`
- **DiscountedAmount**: `double`
- **Name**: `string`
- **Description**: `string`
- **IsCashSale**: `int`
- **HasBeenPaidFor**: `int`
- **Expr2**: `string`
- **LetterHead**: `string`
- **GroupAccountID**: `int`
- **Expr3**: `string`

## tblarinvoicecorporatedetailsDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.AccountsDatasets/_DsMedicalInvoiceInpatient.cs)_
- **ArInvoiceCorporateDetailID**: `int`
- **ArInvoiceID**: `int`
- **DateTimeOfAdmission**: `DateTime`
- **DateTimeOfDischarge**: `DateTime`
- **OutPatientNo**: `int`
- **InPatientNo**: `int`
- **DoctorName**: `string`
- **Sponsor**: `string`
- **PrincipalMember**: `string`
- **MembershipNo**: `string`
- **CompanyName**: `string`
- **Terms**: `string`

## visitRegisterDataTable  _(from HanmakTechnologies.HealthCare.MedicentreV2.DataSets.PatientDataSets/_DsVisitRegister.cs)_
- **Doctor**: `string`
- **Age**: `int`
- **VisitDateTime**: `DateTime`
- **Surname**: `string`
- **OtherNames**: `string`
- **PatientID**: `int`
- **Sex**: `string`
- **DateOfBirth**: `DateTime`
- **Residence**: `string`
- **HospitalInfoID**: `int`
- **Name**: `string`
- **LetterHead**: `string`
- **IsRevisit**: `int`
