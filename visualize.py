import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import base64
import io
import os

def generate_chart(input_data):
    csv_path = input_data.get('csvPath', 'International_Education_Costs_with_Calculations.csv')
    chart_type = input_data.get('chartType', 'heatmap')
    
    if not os.path.isabs(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), csv_path)
    df = pd.read_csv(csv_path)
    
    # Plotly charts
    if chart_type in ['boxplot', 'scatter', 'pie', 'bubble', 'treemap', 'sunburst', 'parallel', 'funnel', 'sankey', 'gauge', 'radar', 'area']:
        if chart_type == 'boxplot':
            fig = px.box(df, x="Country", y="Living_Cost_Index", title="Living Cost by Country")
        elif chart_type == 'scatter':
            fig = px.scatter(df, x="Tuition_USD", y="Total Annual Cost (USD)", color="Country", title="Tuition vs Total Cost")
        elif chart_type == 'pie':
            country_counts = df['Country'].value_counts().head(10)
            fig = px.pie(values=country_counts.values, names=country_counts.index, title="Top 10 Countries by Student Count")
        elif chart_type == 'bubble':
            fig = px.scatter(df, x="Tuition_USD", y="Living_Cost_Index", size="Total Annual Cost (USD)", color="Level", title="Multi-Factor Cost Analysis")
        elif chart_type == 'treemap':
            fig = px.treemap(df, path=['Level', 'Country'], values='Total Annual Cost (USD)', title="Cost Hierarchy")
        elif chart_type == 'sunburst':
            fig = px.sunburst(df, path=['Level', 'Country'], values='Total Annual Cost (USD)', title="Cost Breakdown")
        elif chart_type == 'parallel':
            fig = px.parallel_coordinates(df, dimensions=['Duration_Years', 'Tuition_USD', 'Living_Cost_Index', 'Total Annual Cost (USD)'], title="Multi-Dimensional Analysis")
        elif chart_type == 'funnel':
            level_counts = df['Level'].value_counts()
            fig = px.funnel(x=level_counts.values, y=level_counts.index, title="Education Level Distribution")
        elif chart_type == 'sankey':
            # Simple sankey with country to level flow
            countries = df['Country'].value_counts().head(5).index.tolist()
            levels = df['Level'].unique().tolist()
            fig = px.parallel_categories(df[df['Country'].isin(countries)], dimensions=['Country', 'Level'], title="Country to Level Flow")
        elif chart_type == 'area':
            duration_cost = df.groupby('Duration_Years')['Total Annual Cost (USD)'].mean().reset_index()
            fig = px.area(duration_cost, x='Duration_Years', y='Total Annual Cost (USD)', title='Cost Trend Area Chart')
        elif chart_type == 'gauge':
            avg_cost = df['Total Annual Cost (USD)'].mean()
            fig = px.pie(values=[avg_cost, 100000-avg_cost], names=['Average Cost', 'Remaining'], title=f"Average Cost Gauge: ${avg_cost:,.0f}")
        elif chart_type == 'radar':
            # Multi-country radar chart
            countries = df['Country'].value_counts().head(5).index.tolist()
            radar_data = []
            for country in countries:
                country_data = df[df['Country'] == country]
                radar_data.append({
                    'Country': country,
                    'Tuition': country_data['Tuition_USD'].mean()/1000,
                    'Living Cost': country_data['Living_Cost_Index'].mean(),
                    'Rent': country_data['Rent_USD'].mean(),
                    'Duration': country_data['Duration_Years'].mean()
                })
            radar_df = pd.DataFrame(radar_data)
            fig = px.line_polar(radar_df, r='Tuition', theta=['Tuition', 'Living Cost', 'Rent', 'Duration'], 
                               line_close=True, title="Country Cost Profile Radar")
        return {"plotly": fig.to_json()}
    
    # Matplotlib charts
    plt.figure(figsize=(10, 6))
    if chart_type == 'heatmap':
        sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Heatmap")
    elif chart_type == 'histogram':
        plt.hist(df['Tuition_USD'], bins=30, color='skyblue', edgecolor='black')
        plt.title('Tuition Fee Distribution')
        plt.xlabel('Tuition (USD)')
        plt.ylabel('Frequency')
    elif chart_type == 'bar':
        avg_cost = df.groupby('Level')['Total Annual Cost (USD)'].mean()
        avg_cost.plot(kind='bar', color='lightgreen')
        plt.title('Average Cost by Education Level')
        plt.ylabel('Average Cost (USD)')
        plt.xticks(rotation=45)
    elif chart_type == 'violin':
        sns.violinplot(data=df, x='Level', y='Total Annual Cost (USD)')
        plt.title('Cost Distribution by Education Level')
        plt.xticks(rotation=45)
    elif chart_type == 'line':
        duration_avg = df.groupby('Duration_Years')['Total Annual Cost (USD)'].mean()
        plt.plot(duration_avg.index, duration_avg.values, marker='o')
        plt.title('Average Cost by Duration')
        plt.xlabel('Duration (Years)')
        plt.ylabel('Average Cost (USD)')
    elif chart_type == 'area':
        duration_avg = df.groupby('Duration_Years')['Total Annual Cost (USD)'].mean()
        plt.fill_between(duration_avg.index, duration_avg.values, alpha=0.7)
        plt.title('Cost Trend Area Chart')
        plt.xlabel('Duration (Years)')
        plt.ylabel('Average Cost (USD)')
    elif chart_type == 'density':
        sns.kdeplot(data=df, x='Tuition_USD', y='Total Annual Cost (USD)', fill=True)
        plt.title('Cost Density Map')
    elif chart_type == 'ridge':
        for i, level in enumerate(df['Level'].unique()):
            subset = df[df['Level'] == level]['Total Annual Cost (USD)']
            plt.hist(subset, bins=20, alpha=0.7, label=level, density=True)
        plt.title('Cost Distribution by Level')
        plt.legend()
    elif chart_type == 'strip':
        sns.stripplot(data=df, x='Level', y='Total Annual Cost (USD)')
        plt.title('Individual Cost Points')
        plt.xticks(rotation=45)
    elif chart_type == 'swarm':
        sns.swarmplot(data=df.sample(100), x='Level', y='Total Annual Cost (USD)')
        plt.title('Cost Point Swarm')
        plt.xticks(rotation=45)
    elif chart_type == 'joint':
        sns.scatterplot(data=df, x='Tuition_USD', y='Total Annual Cost (USD)')
        plt.title('Tuition vs Total Cost')
    elif chart_type == 'pair':
        numeric_cols = ['Duration_Years', 'Tuition_USD', 'Living_Cost_Index', 'Total Annual Cost (USD)']
        pd.plotting.scatter_matrix(df[numeric_cols], figsize=(10, 10))
        plt.suptitle('Pairwise Comparison')
    elif chart_type == 'facet':
        levels = df['Level'].unique()[:4]
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        for i, level in enumerate(levels):
            ax = axes[i//2, i%2]
            subset = df[df['Level'] == level]
            ax.scatter(subset['Tuition_USD'], subset['Total Annual Cost (USD)'])
            ax.set_title(f'{level} Level')
            ax.set_xlabel('Tuition (USD)')
            ax.set_ylabel('Total Cost (USD)')
        plt.tight_layout()
    elif chart_type == 'waterfall':
        components = ['Tuition_USD', 'Rent_USD', 'Visa_Fee_USD', 'Insurance_USD']
        values = [df[col].mean() for col in components]
        cumsum = [sum(values[:i+1]) for i in range(len(values))]
        plt.bar(components, values)
        plt.title('Average Cost Components')
        plt.xticks(rotation=45)
    elif chart_type == 'radar':
        # Simple radar chart using polar plot
        categories = ['Duration', 'Tuition', 'Living Cost', 'Rent', 'Visa', 'Insurance']
        values = [df['Duration_Years'].mean(), df['Tuition_USD'].mean()/1000, 
                 df['Living_Cost_Index'].mean(), df['Rent_USD'].mean(), 
                 df['Visa_Fee_USD'].mean(), df['Insurance_USD'].mean()]
        angles = [n / float(len(categories)) * 2 * 3.14159 for n in range(len(categories))]
        angles += angles[:1]
        values += values[:1]
        ax = plt.subplot(111, projection='polar')
        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        plt.title('Cost Profile Radar')
    else:
        plt.text(0.5, 0.5, f'Chart type "{chart_type}" not implemented', ha='center', va='center', transform=plt.gca().transAxes)
        plt.title(f'Chart: {chart_type}')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_b64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return {"image": image_b64}

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    result = generate_chart(input_data)
    print(json.dumps(result))