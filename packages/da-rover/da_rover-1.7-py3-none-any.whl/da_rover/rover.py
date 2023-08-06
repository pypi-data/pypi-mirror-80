# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2019 raka2407
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import pandas as pd
import re
import datetime


def add_tc_row_with_type_as_test_manual(octane_tc_df, name, description):
    if octane_tc_df.empty:
        unique_id = 1
        tc_row_as_test_manual_list = [unique_id]  # unique_id
    else:
        unique_id = octane_tc_df.index.max() + 1
        tc_row_as_test_manual_list = [unique_id]  # unique_id
    tc_row_as_test_manual_list.append('test_manual')  # type
    tc_row_as_test_manual_list.append(name)  # name
    tc_row_as_test_manual_list.append('')  # step_type
    tc_row_as_test_manual_list.append(description)  # description
    tc_row_as_test_manual_list.append('')  # step_description
    tc_row_as_test_manual_list.append('')  # test_type
    tc_row_as_test_manual_list.append('')  # product_areas
    tc_row_as_test_manual_list.append('')  # covered_content
    tc_row_as_test_manual_list.append('')  # designer
    tc_row_as_test_manual_list.append('')  # estimated_duration
    tc_row_as_test_manual_list.append('')  # owner
    if octane_tc_df.empty:
        octane_tc_df.loc[1] = tc_row_as_test_manual_list
    else:
        octane_tc_df.loc[octane_tc_df.index.max() + 1] = tc_row_as_test_manual_list
    return unique_id


def add_tc_row_with_type_as_step(octane_tc_df, row_type, step_description):
    tc_row_as_step_list = [octane_tc_df.index.max() + 1]  # unique_id
    tc_row_as_step_list.append('step')  # type
    tc_row_as_step_list.append('')  # name
    if row_type == 'Simple':
        tc_row_as_step_list.append('Simple')  # step_type
    if row_type == 'Validation':
        tc_row_as_step_list.append('Validation')  # step_type
    tc_row_as_step_list.append('')  # description
    if row_type == 'Simple':
        tc_row_as_step_list.append(step_description)  # step_description
    if row_type == 'Validation':
        tc_row_as_step_list.append(step_description)  # step_description
    tc_row_as_step_list.append('')  # test_type
    tc_row_as_step_list.append('')  # product_areas
    tc_row_as_step_list.append('')  # covered_content
    tc_row_as_step_list.append('')  # designer
    tc_row_as_step_list.append('')  # estimated_duration
    tc_row_as_step_list.append('')  # owner
    octane_tc_df.loc[octane_tc_df.index.max() + 1] = tc_row_as_step_list


def add_ts_row_with_type_as_test_suite(octane_ts_df, name):
    if octane_ts_df.empty:
        ts_row_as_test_suite_list = [1]  # unique_id
    else:
        ts_row_as_test_suite_list = [octane_ts_df.index.max() + 1]  # unique_id
    ts_row_as_test_suite_list.append('test_suite')  # type
    ts_row_as_test_suite_list.append(name)  # name
    ts_row_as_test_suite_list.append('')  # test_id
    ts_row_as_test_suite_list.append('')  # product_areas
    ts_row_as_test_suite_list.append('')  # covered_content
    ts_row_as_test_suite_list.append('')  # designer
    ts_row_as_test_suite_list.append('')  # description
    ts_row_as_test_suite_list.append('')  # owner
    ts_row_as_test_suite_list.append('')  # user_tags
    ts_row_as_test_suite_list.append('')  # aaa_udf
    if octane_ts_df.empty:
        octane_ts_df.loc[1] = ts_row_as_test_suite_list
    else:
        octane_ts_df.loc[octane_ts_df.index.max() + 1] = ts_row_as_test_suite_list


def add_row_with_type_as_defect(octane_defects_df, summary, description, detected_by_full_name, assigned_to_full_name,
                                closing_date, close_reason, comments, priority, project, rootcause_category,
                                rootcause_sub_category, severity, status):
    row_as_defect_list = [summary]  # name
    row_as_defect_list.append(description)  # description
    row_as_defect_list.append(detected_by_full_name)  # detected_by_alm_ref_udf
    row_as_defect_list.append(assigned_to_full_name)  # assigned_to_alm_ref_udf
    row_as_defect_list.append(transform_value_for_date(closing_date))  # closed_on
    if not close_reason:
        row_as_defect_list.append(close_reason)  # close_reason_udf
    else:
        row_as_defect_list.append("")  # close_reason_udf
    row_as_defect_list.append(transform_value_for_comments(comments))  # comments_udf
    row_as_defect_list.append(transform_value_for_priority_or_severity(priority))  # priority
    row_as_defect_list.append(project)  # application_modules
    row_as_defect_list.append(rootcause_category)  # root_cause_category_udf
    if rootcause_category and rootcause_category != "":
        if re.search(rootcause_category, 'Code', re.IGNORECASE):
            root_cause_sub_category_updated = transform_value_for_root_cause_sub_category_code(rootcause_sub_category)
            row_as_defect_list.append(root_cause_sub_category_updated)  # rootcause_subcategory_udf
        if re.search(rootcause_category, 'Configuration Management', re.IGNORECASE):
            root_cause_sub_category_updated = transform_value_for_root_cause_sub_category_configuration_management(
                rootcause_sub_category)
            row_as_defect_list.append(root_cause_sub_category_updated)  # rootcause_subcategory_udf
        if re.search(rootcause_category, 'Design', re.IGNORECASE):
            root_cause_sub_category_updated = transform_value_for_root_cause_sub_category_design(rootcause_sub_category)
            row_as_defect_list.append(root_cause_sub_category_updated)  # rootcause_subcategory_udf
        if re.search(rootcause_category, 'Environment', re.IGNORECASE):
            root_cause_sub_category_updated = transform_value_for_root_cause_sub_category_environment(
                rootcause_sub_category)
            row_as_defect_list.append(root_cause_sub_category_updated)  # rootcause_subcategory_udf
        if re.search(rootcause_category, 'Requirement', re.IGNORECASE):
            root_cause_sub_category_updated = transform_value_for_root_cause_sub_category_requirement(
                rootcause_sub_category)
            row_as_defect_list.append(root_cause_sub_category_updated)  # rootcause_subcategory_udf
        if re.search(rootcause_category, 'Testing', re.IGNORECASE):
            root_cause_sub_category_updated = transform_value_for_root_cause_sub_category_testing(
                rootcause_sub_category)
            row_as_defect_list.append(root_cause_sub_category_updated)  # rootcause_subcategory_udf
    if rootcause_category is "":
        row_as_defect_list.append("")  # rootcause_subcategory_udf

    row_as_defect_list.append(transform_value_for_priority_or_severity(severity))  # severity
    row_as_defect_list.append(transform_value_for_status(status))  # phase
    if octane_defects_df.empty:
        octane_defects_df.loc[1] = row_as_defect_list
    else:
        octane_defects_df.loc[octane_defects_df.index.max() + 1] = row_as_defect_list


def add_ts_row_with_type_as_test_manual(octane_ts_df, test_id):
    ts_row_as_test_manual_list = [octane_ts_df.index.max() + 1]  # unique_id
    ts_row_as_test_manual_list.append('test_manual')  # type
    ts_row_as_test_manual_list.append('')  # name
    ts_row_as_test_manual_list.append(test_id)  # test_id
    ts_row_as_test_manual_list.append('')  # product_areas
    ts_row_as_test_manual_list.append('')  # covered_content
    ts_row_as_test_manual_list.append('')  # designer
    ts_row_as_test_manual_list.append('')  # description
    ts_row_as_test_manual_list.append('')  # owner
    ts_row_as_test_manual_list.append('')  # user_tags
    ts_row_as_test_manual_list.append('')  # aaa_udf
    if octane_ts_df.empty:
        octane_ts_df.loc[1] = ts_row_as_test_manual_list
    else:
        octane_ts_df.loc[octane_ts_df.index.max() + 1] = ts_row_as_test_manual_list


def write_df_to_excel(target_file, octane_tc_df, octane_ts_df, octane_defects_df):
    with pd.ExcelWriter(target_file) as writer:
        if octane_tc_df is not None:
            octane_tc_df.to_excel(writer, sheet_name='manual tests', index=False)
        if octane_ts_df is not None:
            octane_ts_df.to_excel(writer, sheet_name='test suites', index=False)
        if octane_defects_df is not None:
            octane_defects_df.to_excel(writer, sheet_name='defects', index=False)
    print("Transformation completed")


def transform_ard_to_octane(options):
    path = os.path.abspath(os.path.expanduser(options.path))
    source_file_name = options.input
    target_file_name = options.output
    source_file = os.path.join(path, source_file_name)
    target_file = os.path.join(path, target_file_name)
    octane_tc_df = pd.DataFrame(
        columns=['unique_id', 'type', 'name', 'step_type', 'description', 'step_description', 'test_type',
                 'product_areas', 'covered_content', 'designer', 'estimated_duration', 'owner'])
    octane_ts_df = pd.DataFrame(
        columns=['unique_id', 'type', 'name', 'test_id', 'product_areas', 'covered_content', 'designer',
                 'description', 'owner', 'user_tags', 'aaa_udf'])

    print("Transformation started.....please wait")
    ard_df = pd.read_excel(source_file)
    ard_extracted_df = ard_df[['Test Name', 'Description', 'Step Description', 'Expected Result', 'Test Suite']]

    # Iterate through ARD data frame
    for index, row in ard_extracted_df.iterrows():
        # Find if row['Test Name'] exists in DF; ignore if exists; add to DF with incremented index
        if row['Test Name'] not in octane_tc_df.values:
            # Row with type as 'test_manual'
            unique_id = add_tc_row_with_type_as_test_manual(octane_tc_df, row['Test Name'], row['Description'])

            if row['Test Suite'] not in octane_ts_df.values:
                add_ts_row_with_type_as_test_suite(octane_ts_df, row['Test Suite'])
            add_ts_row_with_type_as_test_manual(octane_ts_df, unique_id)

        # Row with type as 'step' and step_type as 'Simple'
        add_tc_row_with_type_as_step(octane_tc_df, "Simple", row['Step Description'])

        # Row with type as 'step' and step_type as 'Validation'
        add_tc_row_with_type_as_step(octane_tc_df, "Validation", row['Expected Result'])

    write_df_to_excel(target_file, octane_tc_df, octane_ts_df, None)


def transform_alm_tc_to_octane(options):
    path = os.path.abspath(os.path.expanduser(options.path))
    source_file_name = options.input
    target_file_name = options.output
    source_file = os.path.join(path, source_file_name)
    target_file = os.path.join(path, target_file_name)
    octane_tc_df = pd.DataFrame(
        columns=['unique_id', 'type', 'name', 'step_type', 'description', 'step_description', 'test_type',
                 'product_areas', 'covered_content', 'designer', 'estimated_duration', 'owner'])
    octane_ts_df = pd.DataFrame(
        columns=['unique_id', 'type', 'name', 'test_id', 'product_areas', 'covered_content', 'designer',
                 'description', 'owner', 'user_tags', 'aaa_udf'])

    print("Transformation started.....please wait")
    alm_df = pd.read_excel(source_file)
    alm_extracted_df = alm_df[['Test Name', 'Description', 'Action', 'Expected Result']]

    # Iterate through ARD data frame
    for index, row in alm_extracted_df.iterrows():
        # Find if row['Test Name'] exists in DF; ignore if exists; add to DF with incremented index
        if row['Test Name'] not in octane_tc_df.values:
            # Row with type as 'test_manual'
            unique_id = add_tc_row_with_type_as_test_manual(octane_tc_df, row['Test Name'], row['Description'])

        # Row with type as 'step' and step_type as 'Simple'
        add_tc_row_with_type_as_step(octane_tc_df, "Simple", row['Action'])

        # Row with type as 'step' and step_type as 'Validation'
        add_tc_row_with_type_as_step(octane_tc_df, "Validation", row['Expected Result'])

    write_df_to_excel(target_file, octane_tc_df, octane_ts_df, None)


def transform_alm_defects_to_octane(options):
    path = os.path.abspath(os.path.expanduser(options.path))
    source_file_name = options.input
    target_file_name = options.output
    source_file = os.path.join(path, source_file_name)
    target_file = os.path.join(path, target_file_name)
    octane_defects_df = pd.DataFrame(
        columns=['name', 'description', 'detected_by_alm_ref_udf', 'assigned_to_alm_ref_udf', 'closed_on',
                 'close_reason_udf', 'comments_udf', 'priority', 'application_modules', 'root_cause_category_udf',
                 'rootcause_subcategory_udf', 'severity', 'phase'])

    print("Transformation started.....please wait")
    alm_df = pd.read_excel(source_file)
    alm_extracted_df = alm_df[
        ['summary', 'description', 'detected_by_full_name', 'detected_in_cycle', 'detected_in_release',
         'assigned_to_full_name', 'closing_date', 'close_reason', 'comments', 'priority', 'source_project',
         'rootcause_category', 'rootcause_sub_category', 'severity', 'status']]

    # Replace NaN with "" in the DF
    alm_extracted_df = alm_extracted_df.fillna("")

    # Iterate through ARD data frame
    for index, row in alm_extracted_df.iterrows():
        # Find if row['summary'] exists in DF; ignore if exists; add to DF with incremented index
        if row['summary'] not in octane_defects_df.values:
            add_row_with_type_as_defect(octane_defects_df, row['summary'], row['description'],
                                        row['detected_by_full_name'],
                                        row['assigned_to_full_name'], row['closing_date'], row['close_reason'],
                                        row['comments'], row['priority'], row['source_project'],
                                        row['rootcause_category'], row['rootcause_sub_category'], row['severity'],
                                        row['status'])

    write_df_to_excel(target_file, None, None, octane_defects_df)


def transform_value_for_priority_or_severity(value):
    # Tranformation of field values for Priority (ALM) or Severity (ALM) to Priority (Octane) or Severity (Octane)
    if re.search(value, '1-Low', re.IGNORECASE):
        return 'Low'
    if re.search(value, '2-Medium', re.IGNORECASE):
        return 'Medium'
    if re.search(value, '3-High', re.IGNORECASE):
        return 'High'
    if re.search(value, '4-Urgent', re.IGNORECASE):
        return 'Urgent'
    if re.search(value, '4-Critical', re.IGNORECASE):
        return 'Critical'


def transform_value_for_comments(value):
    # Tranformation of field values for Comments. Replace ',' with ';'
    return value.replace(',', ';')


def transform_value_for_date(value):
    # Transformation of field value for Closing Date (ALM) to Closed On (Octane)
    # Implement the logic to transform the date format.
    # For Example
    # ALM Value     :       09.08.2019  00:00:00
    # Octane Values :       2015-05-12T10:15:30+01:00
    #                       2015-05-12T10:15:30Z
    #                       2015-05-12T10:15:30+01:00[Europe/Paris]
    #                       2015-05-12T10:15:30+00:00[Z]

    # return datetime.datetime.strptime(str(value), '%d.%m.%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')
    # return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')
    return (datetime.datetime.strptime("2019-07-24 10:11:12", '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ'))


def transform_value_for_status(value):
    # Transformation of field value for Status (ALM) to Phase (Octane)
    if re.search(value, 'In Dispute', re.IGNORECASE):
        return 'In dispute'
    if re.search(value, 'In Progress', re.IGNORECASE):
        return 'In progress'
    if re.search(value, 'Reject', re.IGNORECASE):
        return 'Rejected'
    else:
        return value


def transform_value_for_root_cause_sub_category_code(value):
    if re.search(value, 'Data Inconsistency', re.IGNORECASE):
        return 'Data inconsistency (Code)'
    if re.search(value, 'Incorrect Implementation', re.IGNORECASE):
        return 'Incorrect implementation (Code)'
    if re.search(value, 'Missing Exception Handling', re.IGNORECASE):
        return 'Missing exception handling (Code)'
    if re.search(value, 'Missing Implementation', re.IGNORECASE):
        return 'Missing implementation (Code)'


def transform_value_for_root_cause_sub_category_configuration_management(value):
    if re.search(value, 'Configuration', re.IGNORECASE):
        return 'Configuration (Configuration)'
    if re.search(value, 'Deployment', re.IGNORECASE):
        return 'Deployment (Configuration)'
    if re.search(value, 'Incomplete Operation Documentation', re.IGNORECASE):
        return 'Incomplete Operation documentation (Configuration)'
    if re.search(value, 'Missing Operational Documentation', re.IGNORECASE):
        return 'Missing Operational documentation (Configuration)'
    if re.search(value, 'Version Control', re.IGNORECASE):
        return 'Version control (Configuration)'


def transform_value_for_root_cause_sub_category_design(value):
    if re.search(value, 'Incomplete Design', re.IGNORECASE):
        return 'Incomplete design (Design)'
    if re.search(value, 'Incorrect Design', re.IGNORECASE):
        return 'Incorrect design (Design)'
    if re.search(value, 'Missing Design', re.IGNORECASE):
        return 'Missing design (Design)'


def transform_value_for_root_cause_sub_category_environment(value):
    if re.search(value, '3rd Party', re.IGNORECASE):
        return '3rd Party (Environment)'
    if re.search(value, 'Application Not Available', re.IGNORECASE):
        return 'Application is not available (Environment)'
    if re.search(value, 'Capacity', re.IGNORECASE):
        return 'Capacity (Environment)'
    if re.search(value, 'Certificate', re.IGNORECASE):
        return 'Certificate (Environment)'
    if re.search(value, 'Communication', re.IGNORECASE):
        return 'Communication (Environment)'
    if re.search(value, 'Connectivity', re.IGNORECASE):
        return 'Connectivity (Environment)'
    if re.search(value, 'Data Inconsistency', re.IGNORECASE):
        return 'Data inconsistence (Environment)'
    if re.search(value, 'License', re.IGNORECASE):
        return 'License (Environment)'
    if re.search(value, 'Other Application or Routine', re.IGNORECASE):
        return 'Other application or routine (Environment)'
    if re.search(value, 'Restart', re.IGNORECASE):
        return 'Restart (Environment)'
    if re.search(value, 'Restore', re.IGNORECASE):
        return 'Restore (Environment)'
    if re.search(value, 'Rollback', re.IGNORECASE):
        return 'Rollback (Environment)'
    if re.search(value, 'Table/Disk Space', re.IGNORECASE):
        return 'Table/Disk Space (Environment)'
    if re.search(value, 'Tools', re.IGNORECASE):
        return 'Tools (Environment)'


def transform_value_for_root_cause_sub_category_requirement(value):
    if re.search(value, 'Incomplete Requirements', re.IGNORECASE):
        return 'Incomplete requirement (Requirement)'
    if re.search(value, 'Incorrect Requirements', re.IGNORECASE):
        return 'Incorrect requirement (Requirement)'
    if re.search(value, 'Missing Requirements', re.IGNORECASE):
        return 'Missing requirement (Requirement)'
    if re.search(value, 'Requirements Not Testable', re.IGNORECASE):
        return 'Requirement not testable (Requirement)'


def transform_value_for_root_cause_sub_category_testing(value):
    if re.search(value, 'Incorrect Test Script', re.IGNORECASE):
        return 'Incorrect test script (Testing)'
    if re.search(value, 'Not Applicable Test Case', re.IGNORECASE):
        return 'Not applicable test case (Testing)'
    if re.search(value, 'Role and Permission', re.IGNORECASE):
        return 'Role and permission (Testing)'
    if re.search(value, 'Test Data', re.IGNORECASE):
        return 'Test data (Testing)'
    if re.search(value, 'Tester Error', re.IGNORECASE):
        return 'Tester error (Testing)'
