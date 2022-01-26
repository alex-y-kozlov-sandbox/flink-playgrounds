from pyflink.table import (
    DataTypes, TableEnvironment, EnvironmentSettings, 
    CsvTableSource, CsvTableSink, WriteMode
)

def main():
    env_settings = EnvironmentSettings.new_instance()\
                        .in_batch_mode()\
                        .use_blink_planner()\
                        .build()
    tbl_env = TableEnvironment.create(env_settings)

    in_field_names = ['seller_id', 'product', 'quantity', 'product_price', 'sales_date']
    in_field_types = [DataTypes.STRING(), DataTypes.STRING(), DataTypes.INT(), DataTypes.DOUBLE(), DataTypes.DATE()]
    source = CsvTableSource(
        '/opt/table-api/data/dental-hygiene-orders.csv',
        in_field_names,
        in_field_types,
        ignore_first_line=True
    )
    tbl_env.register_table_source('locale_product_sales', source)

    out_field_names = ['seller_id', 'revenue']
    out_field_types = [DataTypes.STRING(), DataTypes.DOUBLE()]
    sink = CsvTableSink(
        out_field_names,
        out_field_types,
        '/opt/table-api/data/revenue.csv',
        num_files=1,
        write_mode=WriteMode.OVERWRITE
    )
    tbl_env.register_table_sink('locale_revenue', sink)

    sql = """
      SELECT t.seller_id AS seller_id, SUM(t.sales) AS revenue
      FROM (
          SELECT seller_id, product, quantity, product_price, sales_date,
              quantity * product_price AS sales
          FROM locale_product_sales
      ) t
      GROUP BY t.seller_id
    """

    output_tbl = tbl_env.sql_query(sql)

    print('\nLocale Revenue Schema')
    output_tbl.print_schema()

    output_tbl.execute_insert('locale_revenue').wait()


if __name__ == '__main__':
    main()